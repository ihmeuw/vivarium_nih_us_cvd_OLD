from datetime import date
import typing

import pandas as pd
from vivarium_public_health.disease import (DiseaseState as DiseaseState_, DiseaseModel, SusceptibleState,
                                            TransientDiseaseState, RateTransition as RateTransition_)

from vivarium_nih_us_cvd.constants import data_keys, models, models

if typing.TYPE_CHECKING:
    from vivarium.framework.engine import Builder
    from vivarium.framework.population import SimulantData
    from vivarium.framework.event import Event


class RateTransition(RateTransition_):
    def load_transition_rate_data(self, builder):
        if 'transition_rate' in self._get_data_functions:
            rate_data = self._get_data_functions['transition_rate'](builder, self.input_state.cause,
                                                                    self.output_state.cause)
            pipeline_name = f'{self.input_state.cause}_to_{self.output_state.cause}.transition_rate'
        else:
            raise ValueError("No valid data functions supplied.")
        return rate_data, pipeline_name


class DiseaseState(DiseaseState_):

    # I really need to rewrite the state machine code.  It's super inflexible
    def add_transition(self, output, source_data_type=None, get_data_functions=None, **kwargs):
        if source_data_type == 'rate':
            if get_data_functions is None or 'transition_rate' not in get_data_functions:
                raise ValueError('Must supply get data functions for transition_rate.')
            t = RateTransition(self, output, get_data_functions, **kwargs)
            self.transition_set.append(t)
        else:
            t = super().add_transition(output, source_data_type, get_data_functions, **kwargs)
        return t


def IschemicHeartDisease():
    susceptible = SusceptibleState(models.IHD_MODEL_NAME)
    data_funcs = {'dwell_time': lambda *args: pd.Timedelta(days=28)}
    acute_mi = DiseaseState(models.ACUTE_MI_STATE_NAME, cause_type='cause', get_data_functions=data_funcs)
    post_mi = DiseaseState(models.POST_MI_STATE_NAME, cause_type='cause',)
    angina_mi = DiseaseState(models.ANGINA_STATE_NAME, cause_type='cause',)

    susceptible.allow_self_transitions()
    data_funcs = {
        'incidence_rate': lambda _, builder: builder.data.load(data_keys.IHD.MI_ACUTE_INCIDENCE),
        'incidence_rate_angina': lambda _, builder: builder.data.load(data_keys.IHD.ANGINA_INCIDENCE)
    }
    susceptible.add_transition(acute_mi, source_data_type='rate', get_data_functions=data_funcs)
    susceptible.add_transition(angina_mi, source_data_type='rate', get_data_functions=data_funcs)
    acute_mi.allow_self_transitions()
    acute_mi.add_transition(post_mi)
    post_mi.allow_self_transitions()
    data_funcs = {
        'transition_rate': lambda builder, *_: builder.data.load(data_keys.IHD.MI_POST_INCIDENCE),
    }
    post_mi.add_transition(acute_mi, source_data_type='rate', get_data_functions=data_funcs)

    return DiseaseModel(models.IHD_MODEL_NAME, states=[susceptible, acute_mi, post_mi, angina_mi])


def IschemicStroke():
    susceptible = SusceptibleState(models.ISCHEMIC_STROKE_MODEL_NAME)
    data_funcs = {'dwell_time': lambda *args: pd.Timedelta(days=28)}
    acute_stroke = DiseaseState(models.ACUTE_ISCHEMIC_STROKE_STATE_NAME, cause_type='sequela', get_data_functions=data_funcs)
    chronic_stroke = DiseaseState(models.CHRONIC_ISCHEMIC_STROKE_STATE_NAME, cause_type='sequela',)

    susceptible.allow_self_transitions()
    data_funcs = {
        'incidence_rate': lambda _, builder: builder.data.load(data_keys.ISCHEMIC_STROKE.ACUTE_INCIDENCE)
    }
    susceptible.add_transition(acute_stroke, source_data_type='rate', get_data_functions=data_funcs)
    acute_stroke.allow_self_transitions()
    acute_stroke.add_transition(chronic_stroke)
    chronic_stroke.allow_self_transitions()
    data_funcs = {
        'transition_rate': lambda builder, *_: builder.data.load(data_keys.ISCHEMIC_STROKE.ACUTE_INCIDENCE)
    }
    chronic_stroke.add_transition(acute_stroke, source_data_type='rate', get_data_functions=data_funcs)

    return DiseaseModel(models.ISCHEMIC_STROKE_MODEL_NAME, states=[susceptible, acute_stroke, chronic_stroke])
