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
    CSMR: str = f'cause.{mod.IHD_MODEL_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS: str = f'cause.{mod.IHD_MODEL_NAME}.restrictions'
    # Note non-colon construction
    CSMR_ANGINA = f'cause.{mod.ANGINA_STATE_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS_ANGINA = f'cause.{mod.ANGINA_STATE_NAME}.restrictions'

    MI_ACUTE_PREV: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.prevalence' 
    MI_POST_PREV: str = f'cause.{mod.POST_MI_STATE_NAME}.prevalence' 
    ANGINA_PREV: str = f'cause.{mod.ANGINA_STATE_NAME}.prevalence'

    MI_ACUTE_INCIDENCE: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.incidence_rate' 
    MI_POST_INCIDENCE: str = f'cause.{mod.POST_MI_STATE_NAME}.incidence_rate' 
    ANGINA_INCIDENCE: str = f'cause.{mod.ANGINA_STATE_NAME}.incidence_rate'

    MI_ACUTE_EMR: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.excess_mortality_rate'
    MI_POST_EMR: str = f'cause.{mod.POST_MI_STATE_NAME}.excess_mortality_rate'
    ANGINA_EMR: str = f'cause.{mod.ANGINA_STATE_NAME}.excess_mortality_rate'

    MI_ACUTE_DW: str = f'cause.{mod.ACUTE_MI_STATE_NAME}.disability_weight'
    MI_POST_DW: str = f'cause.{mod.POST_MI_STATE_NAME}.disability_weight'
    ANGINA_DW: str = f'cause.{mod.ANGINA_STATE_NAME}.disability_weight'

    @property
    def name(self):
        return mod.IHD_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


IHD = __IHD()


class __IschemicStroke(NamedTuple):
    CSMR: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.restrictions'
    ACUTE_INCIDENCE: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.incidence_rate'

    ACUTE_PREV: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.prevalence' 
    CHRONIC_PREV: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.prevalence'

    ACUTE_EMR: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'
    CHRONIC_EMR: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'

    ACUTE_DW: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'
    CHRONIC_DW: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'

    @property
    def name(self):
        return mod.ISCHEMIC_STROKE_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


ISCHEMIC_STROKE = __IschemicStroke()


class __HighLDLCholesterol(NamedTuple):
    DISTRIBUTION: str = 'risk_factor.high_ldl_cholesterol.distribution'
    EXPOSURE_MEAN: str = 'risk_factor.high_ldl_cholesterol.exposure'
    EXPOSURE_SD: str = 'risk_factor.high_ldl_cholesterol.exposure_standard_deviation'
    EXPOSURE_WEIGHTS: str = 'risk_factor.high_ldl_cholesterol.exposure_distribution_weights'
    RELATIVE_RISK: str = 'risk_factor.high_ldl_cholesterol.relative_risk'
    PAF: str = 'risk_factor.high_ldl_cholesterol.population_attributable_fraction'
    TMRED: str = 'risk_factor.high_ldl_cholesterol.tmred'
    RELATIVE_RISK_SCALAR: str = 'risk_factor.high_ldl_cholesterol.relative_risk_scalar'

    @property
    def name(self):
        return 'high_ldl_cholesterol'

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


LDL_C = __HighLDLCholesterol()


class __HighSystolicBloodPressure(NamedTuple):
    DISTRIBUTION: str = 'risk_factor.high_systolic_blood_pressure.distribution'
    EXPOSURE_MEAN: str = 'risk_factor.high_systolic_blood_pressure.exposure'
    EXPOSURE_SD: str = 'risk_factor.high_systolic_blood_pressure.exposure_standard_deviation'
    EXPOSURE_WEIGHTS: str = 'risk_factor.high_systolic_blood_pressure.exposure_distribution_weights'
    RELATIVE_RISK: str = 'risk_factor.high_systolic_blood_pressure.relative_risk'
    PAF: str = 'risk_factor.high_systolic_blood_pressure.population_attributable_fraction'
    TMRED: str = 'risk_factor.high_systolic_blood_pressure.tmred'
    RELATIVE_RISK_SCALAR: str = 'risk_factor.high_systolic_blood_pressure.relative_risk_scalar'

    @property
    def name(self):
        return 'high_systolic_blood_pressure'

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


SBP = __HighSystolicBloodPressure()


class __FastingPlasmaGlucose(NamedTuple):
    DISTRIBUTION: str = 'risk_factor.high_fasting_plasma_glucose.distribution'
    EXPOSURE_MEAN: str = 'risk_factor.high_fasting_plasma_glucose.exposure'
    EXPOSURE_SD: str = 'risk_factor.high_fasting_plasma_glucose.exposure_standard_deviation'
    EXPOSURE_WEIGHTS: str = 'risk_factor.high_fasting_plasma_glucose.exposure_distribution_weights'
    RELATIVE_RISK: str = 'risk_factor.high_fasting_plasma_glucose.relative_risk'
    PAF: str = 'risk_factor.high_fasting_plasma_glucose.population_attributable_fraction'
    TMRED: str = 'risk_factor.high_fasting_plasma_glucose_continuous.tmred'
    TMRED_LOCAL = 'risk_factor.high_fasting_plasma_glucose.tmred'
    RELATIVE_RISK_SCALAR: str = 'risk_factor.high_fasting_plasma_glucose_continuous.relative_risk_scalar'
    RELATIVE_RISK_SCALAR_LOCAL = 'risk_factor.high_fasting_plasma_glucose.relative_risk_scalar'

    @property
    def name(self):
        return 'high_fasting_plasma_glucose'

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


FPG = __FastingPlasmaGlucose()


class __BMI(NamedTuple):
    DISTRIBUTION: str = 'risk_factor.high_body_mass_index_in_adults.distribution'
    EXPOSURE_MEAN: str = 'risk_factor.high_body_mass_index_in_adults.exposure'
    EXPOSURE_SD: str = 'risk_factor.high_body_mass_index_in_adults.exposure_standard_deviation'
    EXPOSURE_WEIGHTS: str = 'risk_factor.high_body_mass_index_in_adults.exposure_distribution_weights'
    RELATIVE_RISK: str = 'risk_factor.high_body_mass_index_in_adults.relative_risk'
    PAF: str = 'risk_factor.high_body_mass_index_in_adults.population_attributable_fraction'
    TMRED: str = 'risk_factor.high_body_mass_index_in_adults.tmred'
    RELATIVE_RISK_SCALAR: str = 'risk_factor.high_body_mass_index_in_adults.relative_risk_scalar'

    @property
    def name(self):
        return 'high_body_mass_index_in_adults'

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


BMI = __BMI()


MAKE_ARTIFACT_KEY_GROUPS = [
    POPULATION,
    IHD,
    ISCHEMIC_STROKE,
    LDL_C,
    SBP,
    BMI,
    FPG,
]
