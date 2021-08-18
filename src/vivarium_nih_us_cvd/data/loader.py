"""Loads, standardizes and validates input data for the simulation.

Abstract the extract and transform pieces of the artifact ETL.
The intent here is to provide a uniform interface around this portion
of artifact creation. The value of this interface shows up when more
complicated data needs are part of the project. See the BEP project
for an example.

`BEP <https://github.com/ihmeuw/vivarium_gates_bep/blob/master/src/vivarium_gates_bep/data/loader.py>`_

.. admonition::

   No logging is done here. Logging is done in vivarium inputs itself and forwarded.
"""
import pandas as pd
from typing import Dict, Tuple, List, Union

from gbd_mapping import causes, covariates, risk_factors, Sequela, ModelableEntity
from vivarium.framework.artifact import EntityKey
from vivarium.framework.artifact.artifact import Artifact
from vivarium_gbd_access import gbd
from vivarium_inputs import globals as vi_globals, interface, utilities as vi_utils, utility_data
from vivarium_inputs.mapping_extension import alternative_risk_factors
from vivarium_nih_us_cvd.constants import data_keys, models


def get_measure_wrapped(entity: ModelableEntity, key: Union[str, data_keys.SourceSink], location: str) -> pd.DataFrame:
    '''
    All calls to get_measure() need to have the location dropped. For the time being,
    simply use this function.
    '''
    return interface.get_measure(entity, key, location).droplevel('location')


def get_key(val: Union[str, data_keys.SourceSink]):
    return val.source if isinstance(val, data_keys.SourceSink) else val


def load_population_location(key: str, location: str) -> str:
    if key != data_keys.POPULATION.LOCATION:
        raise ValueError(f'Unrecognized key {key}')

    return location


def load_population_structure(key: str, location: str) -> pd.DataFrame:
    return interface.get_population_structure(location)


def load_age_bins(key: str, location: str) -> pd.DataFrame:
    return interface.get_age_bins()


def load_demographic_dimensions(key: str, location: str) -> pd.DataFrame:
    return interface.get_demographic_dimensions(location)


def load_theoretical_minimum_risk_life_expectancy(key: str, location: str) -> pd.DataFrame:
    return interface.get_theoretical_minimum_risk_life_expectancy()


def load_standard_data(key: str, location: str) -> pd.DataFrame:
    key = EntityKey(key)
    entity = get_entity(key)
    return get_measure_wrapped(entity, key.measure, location)


def load_metadata(key: str, location: str):
    key = EntityKey(key)
    entity = get_entity(key)
    entity_metadata = entity[key.measure]
    if hasattr(entity_metadata, 'to_dict'):
        entity_metadata = entity_metadata.to_dict()
    return entity_metadata


def load_metadata_mapped(key: str, location: str):
    map = {
        data_keys.FPG.DISTRIBUTION: 'ensemble'
    }
    return map[key]


STD_FUNCS = [
    load_population_location,
    load_population_structure,
    load_age_bins,
    load_demographic_dimensions,
    load_theoretical_minimum_risk_life_expectancy,
    load_standard_data,
    load_metadata,
    load_metadata_mapped
    ]


def get_data(lookup_key: Union[str, data_keys.SourceSink], location: str) -> pd.DataFrame:
    """Retrieves data from an appropriate source.

    Parameters
    ----------
    lookup_key
        The key that will eventually get put in the artifact with
        the requested data.
    location
        The location to get data for.

    Returns
    -------
        The requested data.

    """
    mapping = {
        data_keys.POPULATION.LOCATION: load_population_location,
        data_keys.POPULATION.STRUCTURE: load_population_structure,
        data_keys.POPULATION.AGE_BINS: load_age_bins,
        data_keys.POPULATION.DEMOGRAPHY: load_demographic_dimensions,
        data_keys.POPULATION.TMRLE: load_theoretical_minimum_risk_life_expectancy,
        data_keys.POPULATION.ACMR: load_standard_data,

        data_keys.MI.PREVALENCE_ACUTE: load_prevalence_ihd,
        data_keys.MI.PREVALENCE_POST: load_prevalence_ihd,
        data_keys.MI.INCIDENCE_ACUTE: load_incidence_ihd,
        data_keys.MI.INCIDENCE_POST: load_incidence_ihd,
        data_keys.MI.DW_ACUTE: load_dw_ihd,
        data_keys.MI.DW_POST: load_dw_ihd,
        data_keys.MI.EMR_ACUTE: load_emr,
        data_keys.MI.EMR_POST: load_emr,
        data_keys.MI.CSMR: load_standard_data,
        data_keys.MI.RESTRICTIONS: load_metadata,

        data_keys.ANGINA.PREVALENCE: load_prevalence_ihd,
        data_keys.ANGINA.INCIDENCE: load_incidence_ihd,
        data_keys.ANGINA.EMR: load_emr,
        data_keys.ANGINA.DW: load_dw_ihd,
        data_keys.ANGINA.RESTRICTIONS: load_metadata,
        data_keys.ANGINA.CSMR: load_csmr_angina,

        data_keys.HF_IHD.PREVALENCE: load_prevalence_ihd,
        data_keys.HF_IHD.INCIDENCE: load_incidence_ihd,
        data_keys.HF_IHD.EMR: load_emr,
        data_keys.HF_IHD.DW: load_dw_ihd,
        data_keys.HF_IHD.RESTRICTIONS: load_metadata,
        data_keys.HF_IHD.CSMR: load_standard_data,

        data_keys.ISCHEMIC_STROKE.PREVALENCE_ACUTE: load_prevalence_ischemic_stroke,
        data_keys.ISCHEMIC_STROKE.PREVALENCE_CHRONIC: load_prevalence_ischemic_stroke,

        data_keys.ISCHEMIC_STROKE.DW_ACUTE: load_disability_weight_ischemic_stroke_,
        data_keys.ISCHEMIC_STROKE.DW_CHRONIC: load_disability_weight_ischemic_stroke_,

        data_keys.ISCHEMIC_STROKE.EMR_ACUTE: load_emr_ischemic_stroke,
        data_keys.ISCHEMIC_STROKE.EMR_CHRONIC: load_emr_ischemic_stroke,
        data_keys.ISCHEMIC_STROKE.INCIDENCE_ACUTE: load_standard_data,
        data_keys.ISCHEMIC_STROKE.CSMR: load_standard_data,
        data_keys.ISCHEMIC_STROKE.RESTRICTIONS: load_metadata,

        data_keys.PAD.PREVALENCE: load_standard_data,
        data_keys.PAD.INCIDENCE: load_standard_data,
        data_keys.PAD.DW: load_standard_data,
        data_keys.PAD.EMR: load_standard_data,
        data_keys.PAD.CSMR: load_standard_data,
        data_keys.PAD.RESTRICTIONS: load_metadata,

        data_keys.AFIB.PREVALENCE: load_standard_data,
        data_keys.AFIB.INCIDENCE: load_standard_data,
        data_keys.AFIB.DW: load_standard_data,
        data_keys.AFIB.EMR: load_standard_data,
        data_keys.AFIB.CSMR: load_standard_data,
        data_keys.AFIB.RESTRICTIONS: load_metadata,

        data_keys.LDL_C.DISTRIBUTION: load_metadata,
        data_keys.LDL_C.EXPOSURE_MEAN: load_standard_data,
        data_keys.LDL_C.EXPOSURE_SD: load_standard_data,
        data_keys.LDL_C.EXPOSURE_WEIGHTS: load_standard_data,
        #data_keys.LDL_C.HIGH_RISK_THRESHOLD: load_high_risk_ldl_threshold,
        data_keys.LDL_C.RELATIVE_RISK: load_standard_data,
        data_keys.LDL_C.PAF: load_standard_data,
        data_keys.LDL_C.TMRED: load_metadata,
        data_keys.LDL_C.RELATIVE_RISK_SCALAR: load_metadata,

        data_keys.SBP.DISTRIBUTION: load_metadata,
        data_keys.SBP.EXPOSURE_MEAN: load_standard_data,
        data_keys.SBP.EXPOSURE_SD: load_standard_data,
        data_keys.SBP.EXPOSURE_WEIGHTS: load_standard_data,
        data_keys.SBP.RELATIVE_RISK: load_standard_data,
        data_keys.SBP.PAF: load_standard_data,
        data_keys.SBP.TMRED: load_metadata,
        data_keys.SBP.RELATIVE_RISK_SCALAR: load_metadata,

        data_keys.FPG.DISTRIBUTION: load_metadata_mapped,
        data_keys.FPG.EXPOSURE_MEAN: load_standard_data,
        data_keys.FPG.EXPOSURE_SD: load_standard_data,
        data_keys.FPG.EXPOSURE_WEIGHTS: load_standard_data,
        data_keys.FPG.RELATIVE_RISK: load_standard_data,
        data_keys.FPG.PAF: load_standard_data,
        data_keys.FPG.TMRED: load_metadata,
        data_keys.FPG.RELATIVE_RISK_SCALAR: load_metadata,

        data_keys.BMI.DISTRIBUTION: load_metadata,
        data_keys.BMI.EXPOSURE_MEAN: load_standard_data,
        data_keys.BMI.EXPOSURE_SD: load_standard_data,
        data_keys.BMI.EXPOSURE_WEIGHTS: load_standard_data,
        data_keys.BMI.RELATIVE_RISK: load_standard_data,
        data_keys.BMI.PAF: load_standard_data,
        data_keys.BMI.TMRED: load_metadata,
        data_keys.BMI.RELATIVE_RISK_SCALAR: load_metadata,
    }
    func = mapping[lookup_key]
    if func in STD_FUNCS:
        lookup_key = get_key(lookup_key)
    return func(lookup_key, location)


def _load_em_from_meid(meid: int, measure: str, location: str):
    location_id = utility_data.get_location_id(location)
    data = gbd.get_modelable_entity_draws(meid, location_id)
    data = data[data.measure_id == vi_globals.MEASURES[measure]]
    data = vi_utils.normalize(data, fill_value=0)
    data = data.filter(vi_globals.DEMOGRAPHIC_COLUMNS + vi_globals.DRAW_COLUMNS)
    data = vi_utils.reshape(data)
    data = vi_utils.scrub_gbd_conventions(data, location)
    data = vi_utils.split_interval(data, interval_column='age', split_column_prefix='age')
    data = vi_utils.split_interval(data, interval_column='year', split_column_prefix='year')
    return vi_utils.sort_hierarchical_data(data).droplevel('location')


#
# project-specific data functions here
#
def get_prevalence_weighted_disability_weight(seq: List[Sequela], location: str) -> List[pd.DataFrame]:
    assert len(seq), "Empty List - get_prevalence_weighted_disability_weight()"
    prevalence_disability_weights = []
    for s in seq:
        prevalence = get_measure_wrapped(s, 'prevalence', location)
        disability_weight = get_measure_wrapped(s, 'disability_weight', location)
        prevalence_disability_weights.append(prevalence * disability_weight)
    return prevalence_disability_weights


def get_ihd_sequelae() -> Tuple[Dict[str, List[Sequela]], Dict[int, Sequela]]:
    by_cause = {
        'acute': causes.ischemic_heart_disease.sequelae[:2],
        'post': [causes.ischemic_heart_disease.sequelae[9]],
        'angina': [s for s in causes.ischemic_heart_disease.sequelae if 'angina' in s.name],
        'heart_failure': [s for s in causes.ischemic_heart_disease.sequelae if 'heart_failure' in s.name]
    }

    by_seq_id = {}
    for s in causes.ischemic_heart_disease.sequelae:
        id = int(str(s.gbd_id).split('(')[1][:-1])
        by_seq_id[id] = s

    return by_cause, by_seq_id


def load_prevalence_ihd(key: data_keys.SourceSink, location: str) -> pd.DataFrame:
    ihd_seq, _ = get_ihd_sequelae()
    map = {
        data_keys.MI.PREVALENCE_ACUTE.sink: ihd_seq['acute'],
        data_keys.MI.PREVALENCE_POST.sink: ihd_seq['post'],
        data_keys.ANGINA.PREVALENCE.sink: ihd_seq['angina'],
        data_keys.HF_IHD.PREVALENCE.sink: ihd_seq['heart_failure'],
    }
    return load_prevalence(map[key.sink], location)


def load_prevalence(seq: List[Sequela], location: str) -> pd.DataFrame:
    prevalence = sum(get_measure_wrapped(s, 'prevalence', location) for s in seq)
    return prevalence


def load_incidence_ihd(key: data_keys.SourceSink, location: str) -> pd.DataFrame:
    ihd_seq, _ = get_ihd_sequelae()
    map = {
        data_keys.MI.INCIDENCE_ACUTE.sink: (ihd_seq['acute'], 24694),
        data_keys.MI.INCIDENCE_POST.sink: (ihd_seq['post'], 24694),
        data_keys.ANGINA.INCIDENCE.sink: (ihd_seq['angina'], 1817),
        data_keys.HF_IHD.INCIDENCE.sink: (ihd_seq['heart_failure'], 2412)
    }
    seq, meid = map[key.sink]
    prevalence = sum(get_measure_wrapped(s, 'prevalence', location) for s in seq)
    incidence = _load_em_from_meid(meid, 'Incidence rate', location)
    return incidence / (1 - prevalence)


def load_emr(key: data_keys.SourceSink, location: str) -> pd.DataFrame:
    map = {
        data_keys.MI.EMR_ACUTE.sink: 24694,
        data_keys.MI.EMR_POST.sink: 15755,
        data_keys.ANGINA.EMR.sink: 1817,
        data_keys.HF_IHD.EMR.sink: 2412,
    }
    return _load_em_from_meid(map[key.sink], 'Excess mortality rate', location)


def load_csmr_angina(key: str, location: str) -> pd.DataFrame:
    # Maybe use later... For now use IHD cause_specific_mortality, which contains angina emr,
    #   and make angina csmr be zero. The csmr is necessary to use the default SI model for angina
    # csmr_angina = (load_ihd_prevalence(data_keys.IHD.ANGINA_PREV, location)
    #               * load_ihd_emr(data_keys.IHD.ANGINA_EMR, location))
    #
    # This doesn't work -- can't query sequela for cause_specific_mortality_rate.
    # ihd_seq, _ = get_ihd_sequelae()
    # ang_seq = ihd_seq["angina"]
    # ang_csmr = sum(get_measure_wrapped(s, 'cause_specific_mortality_rate', location) for s in ang_seq)
    # return ang_csmr
    draws = [f'draw_{i}' for i in range(1000)]
    df_zeros = load_emr(data_keys.ANGINA.EMR, location)
    df_zeros[draws] = 0.0
    return df_zeros


def load_dw_ihd(key: data_keys.SourceSink, location: str) -> pd.DataFrame:
    map = {
        data_keys.MI.DW_ACUTE.sink: "acute",
        data_keys.MI.DW_POST.sink: "post",
        data_keys.ANGINA.DW.sink: "angina",
        data_keys.HF_IHD.DW.sink: "heart_failure"
    }
    seq, _ = get_ihd_sequelae()
    term_1 = 1 / load_prevalence(seq[map[key.sink]], location)
    term_2 = get_prevalence_weighted_disability_weight(seq[map[key.sink]], location)
    return term_1 * sum(term_2)


def get_ischemic_stroke_sequelae() ->  Tuple[pd.DataFrame, pd.DataFrame]:
    acute_sequelae = [s for s in causes.ischemic_stroke.sequelae if 'acute' in s.name]
    chronic_sequelae = [s for s in causes.ischemic_stroke.sequelae if 'chronic' in s.name]
    return acute_sequelae, chronic_sequelae


def load_prevalence_ischemic_stroke(key: str, location: str) -> pd.DataFrame:
    acute_sequelae, chronic_sequelae = get_ischemic_stroke_sequelae()
    map = {
        data_keys.ISCHEMIC_STROKE.PREVALENCE_ACUTE: acute_sequelae,
        data_keys.ISCHEMIC_STROKE.PREVALENCE_CHRONIC: chronic_sequelae
    }
    prevalence = sum(get_measure_wrapped(s, 'prevalence', location) for s in map[key])
    return prevalence


def load_disability_weight_ischemic_stroke_(key: str, location: str) -> pd.DataFrame:
    acute_sequelae, chronic_sequelae = get_ischemic_stroke_sequelae()
    map = {
        data_keys.ISCHEMIC_STROKE.DW_ACUTE: acute_sequelae,
        data_keys.ISCHEMIC_STROKE.DW_CHRONIC: chronic_sequelae
    }
    prevalence_disability_weights = get_prevalence_weighted_disability_weight(map[key], location)
    ischemic_stroke_prevalence = get_measure_wrapped(causes.ischemic_stroke, 'prevalence', location)
    ischemic_stroke_disability_weight = (sum(prevalence_disability_weights) / ischemic_stroke_prevalence).fillna(0)
    return ischemic_stroke_disability_weight


def load_emr_ischemic_stroke(key: str, location: str) -> pd.DataFrame:
    map = {
        data_keys.ISCHEMIC_STROKE.EMR_ACUTE: 24714,
        data_keys.ISCHEMIC_STROKE.EMR_CHRONIC: 10837,
    }
    return _load_em_from_meid(map[key], 'Excess mortality rate', location)


def load_high_risk_ldl_threshold(key: str, location: str) -> pd.DataFrame:
    pass
    # TODO:
    # data_path = paths.LDL_C_THRESHOLD_DIR / f'{sanitize_location(location)}.hdf'
    # ldl_exposure = pd.read_hdf(data_path)
    # return ldl_exposure


def modify_rr_affected_entity(art: Artifact, risk_key: str, mod_map: Dict[str, List[str]]) -> None:
    """ Load RR data and duplicate selected rows so that the affected_entity and affected_measure
        columns correspond to what is used in the disease model
    """
    def is_transition_rate(name: str) -> bool:
        """ affected_measure needs to change to "transition_rate" in some cases
        """
        return '_to_' in name

    # Note: not removing original affected_entity rows
    df_orig = art.load(risk_key)
    add_these = []
    for key in mod_map.keys():
        df_flat = df_orig.reset_index()
        add_these.append(df_flat)

        # this is the data to be duplicated
        df_copy = df_flat.query(f'affected_entity=="{key}"')
        for name in mod_map[key]:
            df_new = df_copy.copy()
            df_new.affected_entity = name
            if is_transition_rate(name):
                df_new.affected_measure = 'transition_rate'
            add_these.append(df_new)
    df = pd.concat(add_these, ignore_index=True)
    df = df.set_index([c for c in df.columns if 'draw_' not in c])
    art.replace(risk_key, df)


def handle_special_cases(artifact: Artifact, location: str):
    # artifact.write(data_keys.ANGINA.RESTRICTIONS_ANGINA, artifact.load(data_keys.MI.RESTRICTIONS))
    # Maybe use later... For now use IHD cause_specific_mortality, which contains angina emr,
    #   and make angina csmr be zero. The csmr is necessary to use the default SI model for angina
    # csmr_angina = (load_ihd_prevalence(data_keys.IHD.ANGINA_PREV, location)
    #               * load_ihd_emr(data_keys.IHD.ANGINA_EMR, location))
    # draws = [f'draw_{i}' for i in range(1000)]
    # df_zeros = load_emr(data_keys.ANGINA.ANGINA_EMR, location)
    # df_zeros[draws] = 0.0
    # artifact.write(data_keys.ANGINA.CSMR_ANGINA, df_zeros)


    # Need to make RR data match causes in the model
    map = {
        'ischemic_heart_disease': ['acute_myocardial_infarction', 'post_myocardial_infarction_to_acute_myocardial_infarction', 'heart_failure_from_ihd'],
        models.ISCHEMIC_STROKE_MODEL_NAME: ['acute_ischemic_stroke', 'chronic_ischemic_stroke_to_acute_ischemic_stroke'],
    }
    for key in [
        data_keys.LDL_C.RELATIVE_RISK,
        data_keys.LDL_C.PAF,
        data_keys.SBP.RELATIVE_RISK,
        data_keys.SBP.PAF,
        data_keys.BMI.RELATIVE_RISK,
        data_keys.BMI.PAF,
        data_keys.FPG.RELATIVE_RISK,
        data_keys.FPG.PAF,
    ]:
        modify_rr_affected_entity(artifact, key, map)

    artifact.write(data_keys.FPG.TMRED_LOCAL, artifact.load(data_keys.FPG.TMRED))
    artifact.write(data_keys.FPG.RELATIVE_RISK_SCALAR_LOCAL, artifact.load(data_keys.FPG.RELATIVE_RISK_SCALAR))


def get_entity(key: str):
    # Map of entity types to their gbd mappings.
    type_map = {
        'cause': causes,
        'covariate': covariates,
        'risk_factor': risk_factors,
        'alternative_risk_factor': alternative_risk_factors
    }
    key = EntityKey(key)
    return type_map[key.type][key.name]
