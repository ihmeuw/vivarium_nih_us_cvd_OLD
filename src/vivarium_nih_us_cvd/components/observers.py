import typing
import pandas as pd
import operator as op
from collections import Counter
from functools import reduce
from typing import Dict, Iterable, List, Tuple, NamedTuple
from itertools import product

from vivarium_public_health.metrics import (MortalityObserver as MortalityObserver_,
                                            DisabilityObserver as DisabilityObserver_)
from vivarium_public_health.metrics.utilities import (get_state_person_time, QueryString, 
                                                      get_transition_count, get_age_bins)

from vivarium_nih_us_cvd.constants import data_keys, data_values, models

if typing.TYPE_CHECKING:
    from vivarium.framework.engine import Builder
    from vivarium.framework.event import Event
    from vivarium.framework.population import SimulantData


class MaskAndId(NamedTuple):
    mask: pd.Series
    id: str


class ResultsStratifier:
    """Centralized component for handling results stratification.

    This should be used as a sub-component for observers.  The observers
    can then ask this component for population subgroups and labels during
    results production and have this component manage adjustments to the
    final column labels for the subgroups.

    """

    def __init__(self, observer_name: str):
        self.name = f'{observer_name}_results_stratifier'
        self._risk_group_ids = []

    # noinspection PyAttributeOutsideInit
    def setup(self, builder: 'Builder'):
        """Perform this component's setup."""
        # The only thing you should request here are resources necessary for
        # results stratification.
        self.sbp = builder.value.get_value('high_systolic_blood_pressure.exposure')
        self.ldlc = builder.value.get_value('high_ldl_cholesterol.exposure')
        self.fpg = builder.value.get_value('high_fasting_plasma_glucose.exposure')
        self.bmi = builder.value.get_value('high_body_mass_index_in_adults.exposure')

        columns_required = [models.IHD_MODEL_NAME,
                            models.ISCHEMIC_STROKE_MODEL_NAME]
        self.population_view = builder.population.get_view(columns_required)
        self.risk_groups = None
        builder.population.initializes_simulants(self.on_initialize_simulants,
                                                 requires_columns=columns_required,
                                                 requires_values=['high_systolic_blood_pressure.exposure',
                                                                  'high_ldl_cholesterol.exposure'])

    # noinspection PyAttributeOutsideInit
    def on_initialize_simulants(self, pop_data: 'SimulantData'):
        risk_groups = pd.Series('', index=pop_data.index)
        pop = self.population_view.get(pop_data.index)

        sbp = self.sbp(pop_data.index)
        ldlc = self.ldlc(pop_data.index)
        fpg = self.fpg(pop_data.index)
        bmi = self.bmi(pop_data.index)

        high_sbp = sbp > data_values.THRESHOLD_HIGH_SBP
        high_ldlc = ldlc > data_values.THRESHOLD_HIGH_LDLC
        high_fpg = fpg > data_values.THRESHOLD_HIGH_FPG
        high_bmi = bmi > data_values.THRESHOLD_HIGH_BMI

        groups = []
        groups.append([MaskAndId(high_sbp, 'SBP_high'), MaskAndId(~high_sbp, 'SBP_normal')])
        groups.append([MaskAndId(high_ldlc, 'LDL_high'), MaskAndId(~high_ldlc, 'LDL_normal')])
        groups.append([MaskAndId(high_fpg, 'FPG_high'), MaskAndId(~high_fpg, 'FPG_normal')])
        groups.append([MaskAndId(high_bmi, 'BMI_high'), MaskAndId(~high_bmi, 'BMI_normal')])
        p_groups = product(*groups)

        # This generates a list of concatenated strings from the stratification layers:
        #   "SBP_high_LDL_high_FPG_high_BMI_high"
        self._risk_group_ids = ['_'.join(i) for i in list(product(*[[g[0].id, g[1].id] for g in groups]))]

        for group in p_groups:
            mask = reduce(op.and_, [j.mask for j in group])
            id_str = '_'.join([j.id for j in group])
            risk_groups.loc[mask] = id_str

        self.risk_groups = risk_groups

    def group(self, population: pd.DataFrame) -> Iterable[Tuple[Tuple[str, ...], pd.DataFrame]]:
        """Takes the full population and yields stratified subgroups.

        Parameters
        ----------
        population
            The population to stratify.

        Yields
        ------
            A tuple of stratification labels and the population subgroup
            corresponding to those labels.

        """
        stratification_group = self.risk_groups.loc[population.index]
        for risk_cat in self._risk_group_ids:
            if population.empty:
                pop_in_group = population
            else:
                pop_in_group = population.loc[stratification_group == risk_cat]
            yield (risk_cat,), pop_in_group

    @staticmethod
    def update_labels(measure_data: Dict[str, float], labels: Tuple[str, ...]) -> Dict[str, float]:
        """Updates a dict of measure data with stratification labels.

        Parameters
        ----------
        measure_data
            The measure data with unstratified column names.
        labels
            The stratification labels. Yielded along with the population
            subgroup the measure data was produced from by a call to
            :obj:`ResultsStratifier.group`.

        Returns
        -------
            The measure data with column names updated with the stratification
            labels.

        """
        stratification_label = labels[0]
        measure_data = {f'{k}_{stratification_label}': v for k, v in measure_data.items()}
        return measure_data


class DiseaseObserver:
    """Observes transition counts and person time for a cause."""
    configuration_defaults = {
        'metrics': {
            'disease_observer': {
                'by_age': False,
                'by_year': False,
                'by_sex': False,
            }
        }
    }

    def __init__(self, disease: str):
        self.disease = disease
        self.configuration_defaults = {
            'metrics': {f'{disease}_observer': DiseaseObserver.configuration_defaults['metrics']['disease_observer']}
        }
        self.stratifier = ResultsStratifier(self.name)

    @property
    def name(self) -> str:
        return f'disease_observer.{self.disease}'

    @property
    def sub_components(self) -> List[ResultsStratifier]:
        return [self.stratifier]

    # noinspection PyAttributeOutsideInit
    def setup(self, builder: 'Builder'):
        self.config = builder.configuration['metrics'][f'{self.disease}_observer'].to_dict()
        self.clock = builder.time.clock()
        self.age_bins = get_age_bins(builder)
        self.counts = Counter()
        self.person_time = Counter()

        self.states = models.STATE_MACHINE_MAP[self.disease]['states']
        self.transitions = models.STATE_MACHINE_MAP[self.disease]['transitions']

        self.previous_state_column = f'previous_{self.disease}'
        builder.population.initializes_simulants(self.on_initialize_simulants,
                                                 creates_columns=[self.previous_state_column])

        columns_required = ['alive', f'{self.disease}', self.previous_state_column]
        if self.config['by_age']:
            columns_required += ['age']
        if self.config['by_sex']:
            columns_required += ['sex']
        self.population_view = builder.population.get_view(columns_required)

        builder.value.register_value_modifier('metrics', self.metrics)
        # FIXME: The state table is modified before the clock advances.
        # In order to get an accurate representation of person time we need to look at
        # the state table before anything happens.
        builder.event.register_listener('time_step__prepare', self.on_time_step_prepare)
        builder.event.register_listener('collect_metrics', self.on_collect_metrics)

    def on_initialize_simulants(self, pop_data: 'SimulantData'):
        self.population_view.update(pd.Series('', index=pop_data.index, name=self.previous_state_column))

    def on_time_step_prepare(self, event: 'Event'):
        pop = self.population_view.get(event.index)
        # Ignoring the edge case where the step spans a new year.
        # Accrue all counts and time to the current year.
        for labels, pop_in_group in self.stratifier.group(pop):
            for state in self.states:
                # noinspection PyTypeChecker
                state_person_time_this_step = get_state_person_time(pop_in_group, self.config, self.disease, state,
                                                                    self.clock().year, event.step_size, self.age_bins)
                state_person_time_this_step = self.stratifier.update_labels(state_person_time_this_step, labels)
                self.person_time.update(state_person_time_this_step)

        # This enables tracking of transitions between states
        prior_state_pop = self.population_view.get(event.index)
        prior_state_pop[self.previous_state_column] = prior_state_pop[self.disease]
        self.population_view.update(prior_state_pop)

    def on_collect_metrics(self, event: 'Event'):
        pop = self.population_view.get(event.index)
        for labels, pop_in_group in self.stratifier.group(pop):
            for transition in self.transitions:
                # noinspection PyTypeChecker
                transition_counts_this_step = get_transition_count(pop_in_group, self.config, self.disease, transition,
                                                                   event.time, self.age_bins)
                transition_counts_this_step = self.stratifier.update_labels(transition_counts_this_step, labels)
                self.counts.update(transition_counts_this_step)

    def metrics(self, index: pd.Index, metrics: Dict[str, float]):
        metrics.update(self.counts)
        metrics.update(self.person_time)
        return metrics

    def __repr__(self) -> str:
        return f"DiseaseObserver({self.disease})"
