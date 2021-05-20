from typing import NamedTuple

from vivarium_public_health.utilities import TargetString


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
    CSMR = 'cause.ischemic_heart_disease.cause_specific_mortality_rate'
    MI_ACUTE_PREV: str = 'cause.ihd_mi_acute.prevalence' 
    MI_POST_PREV: str = 'cause.ihd_mi_post.prevalence' 
    ANGINA_PREV: str = 'cause.ihd_mi_angina.prevalence'

    MI_ACUTE_EMR: str = 'cause.ihd_mi_acute.excess_mortality_rate'
    MI_POST_EMR: str = 'cause.ihd_mi_post.excess_mortality_rate'
    ANGINA_EMR: str = 'cause.ihd_mi_angina.excess_mortality_rate'

    MI_ACUTE_DW: str = 'cause.ihd_mi_acute.disability_weight'
    MI_POST_DW: str = 'cause.ihd_mi_post.disability_weight'
    ANGINA_DW: str = 'cause.ihd_mi_angina.disability_weight'

    RESTRICTIONS: str = 'cause.ischemic_heart_disease.restrictions'

    @property
    def name(self):
        return 'ischemic_heart_disease'

    @property
    def log_name(self):
        return 'ischemic heart disease'


IHD = __IHD()


class __IschemicStroke(NamedTuple):
    CSMR: str = 'cause.ischemic_stroke.cause_specific_mortality_rate'

    ACUTE_PREV: str = 'cause.ischemic_stroke_acute.prevalence' 
    CHRONIC_PREV: str = 'cause.ischemic_stroke_chronic.prevalence' 

    ACUTE_EMR: str = 'cause.ischemic_stroke_acute.excess_mortality_rate'
    CHRONIC_EMR: str = 'cause.ischemic_stroke_chronic.excess_mortality_rate'

    ACUTE_DW: str = 'cause.ischemic_stroke_acute.disability_weight'
    CHRONIC_DW: str = 'cause.ischemic_stroke_chronic.disability_weight'

    ACUTE_EMR: str = 'cause.ischemic_stroke_acute.excess_mortality_rate'
    CHRONIC_EMR: str = 'cause.ischemic_stroke_chronic.excess_mortality_rate'

    RESTRICTIONS: str = 'cause.ischemic_stroke.restrictions'

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
