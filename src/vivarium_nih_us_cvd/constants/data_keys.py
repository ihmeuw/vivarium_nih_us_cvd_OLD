from typing import NamedTuple

from vivarium_nih_us_cvd.constants import models as mod

#############
# Data Keys #
#############

METADATA_LOCATIONS = 'metadata.locations'


class __Population(NamedTuple):
    LOCATION: str = 'population.location'
    STRUCTURE: str = 'population.structure'
    AGE_BINS: str = 'population.age_bins'
    DEMOGRAPHY: str = 'population.demographic_dimensions'
    TMRLE: str = 'population.theoretical_minimum_risk_life_expectancy'
    ACMR: str = 'cause.all_causes.cause_specific_mortality_rate'

    @property
    def name(self):
        return 'population'

    @property
    def log_name(self):
        return 'population'


POPULATION = __Population()


class __IHD(NamedTuple):
    CSMR: str = 'cause.ischemic_heart_disease.cause_specific_mortality_rate'
    RESTRICTIONS: str = 'cause.ischemic_heart_disease.restrictions'

    MI_ACUTE_PREV: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.prevalence' 
    MI_POST_PREV: str = f'cause.{mod.POST_MI_STATE_NAME}.prevalence' 
    ANGINA_PREV: str = f'cause.{mod.ANGINA_STATE_NAME}.prevalence'

    MI_ACUTE_INCIDENCE: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.incidence' 
    MI_POST_INCIDENCE: str = f'cause.{mod.POST_MI_STATE_NAME}.incidence' 
    ANGINA_INCIDENCE: str = f'cause.{mod.ANGINA_STATE_NAME}.incidence'

    MI_ACUTE_EMR: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.excess_mortality_rate'
    MI_POST_EMR: str = f'cause.{mod.POST_MI_STATE_NAME}.excess_mortality_rate'
    ANGINA_EMR: str = f'cause.{mod.ANGINA_STATE_NAME}.excess_mortality_rate'

    MI_ACUTE_DW: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.disability_weight'
    MI_POST_DW: str = f'cause.{mod.POST_MI_STATE_NAME}.disability_weight'
    ANGINA_DW: str = f'cause.{mod.ANGINA_STATE_NAME}.disability_weight'

    @property
    def name(self):
        return 'ischemic_heart_disease'

    @property
    def log_name(self):
        return 'ischemic heart disease'


IHD = __IHD()


class __IschemicStroke(NamedTuple):
    CSMR: str = 'cause.ischemic_stroke.cause_specific_mortality_rate'
    RESTRICTIONS: str = 'cause.ischemic_stroke.restrictions'
    ACUTE_INCIDENCE: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.incidence_rate'

    ACUTE_PREV: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.prevalence' 
    CHRONIC_PREV: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.prevalence'

    ACUTE_EMR: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'
    CHRONIC_EMR: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'

    ACUTE_DW: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'
    CHRONIC_DW: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'

    @property
    def name(self):
        return 'ischemic_stroke'

    @property
    def log_name(self):
        return 'ischemic stroke'


ISCHEMIC_STROKE = __IschemicStroke()

MAKE_ARTIFACT_KEY_GROUPS = [
    POPULATION,
    IHD,
    ISCHEMIC_STROKE,
]
