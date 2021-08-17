from typing import NamedTuple

from vivarium_nih_us_cvd.constants import models as mod


class SourceSink(NamedTuple):
    source: str
    sink: str


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


class __MI(NamedTuple):
    CSMR: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.cause_specific_mortality_rate',
        f'cause.{mod.MI_MODEL_NAME}.cause_specific_mortality_rate',
    )
    RESTRICTIONS: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.restrictions', f'cause.{mod.MI_MODEL_NAME}.restrictions'
    )
    PREVALENCE_ACUTE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.prevalence', f'cause.{mod.ACUTE_MI_STATE_NAME}.prevalence'
    )
    PREVALENCE_POST: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.prevalence', f'cause.{mod.POST_MI_STATE_NAME}.prevalence'
    )
    INCIDENCE_ACUTE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.incidence_rate', f'cause.{mod.ACUTE_MI_STATE_NAME}.incidence_rate'
    )
    INCIDENCE_POST: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.incidence_rate', f'cause.{mod.POST_MI_STATE_NAME}.incidence_rate'
    )
    EMR_ACUTE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.excess_mortality_rate',
        f'cause.{mod.ACUTE_MI_STATE_NAME}.excess_mortality_rate',
    )
    EMR_POST: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.excess_mortality_rate',
        f'cause.{mod.POST_MI_STATE_NAME}.excess_mortality_rate',
    )
    DW_ACUTE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.disability_weight', f'cause.{mod.ACUTE_MI_STATE_NAME}.disability_weight'
    )
    DW_POST: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.disability_weight', f'cause.{mod.POST_MI_STATE_NAME}.disability_weight'
    )

    @property
    def name(self):
        return mod.MI_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


MI = __MI()


class __ANGINA(NamedTuple):
    CSMR: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.cause_specific_mortality_rate',
        f'cause.{mod.ANGINA_MODEL_NAME}.cause_specific_mortality_rate',
    )
    RESTRICTIONS: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.restrictions', f'cause.{mod.ANGINA_MODEL_NAME}.restrictions'
    )
    PREVALENCE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.prevalence', f'cause.{mod.ANGINA_MODEL_NAME}.prevalence'
    )
    INCIDENCE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.incidence_rate', f'cause.{mod.ANGINA_MODEL_NAME}.incidence_rate'
    )
    EMR: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.excess_mortality_rate',
        f'cause.{mod.ANGINA_MODEL_NAME}.excess_mortality_rate',
    )
    DW: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.disability_weight', f'cause.{mod.ANGINA_MODEL_NAME}.disability_weight'
    )

    @property
    def name(self):
        return mod.ANGINA_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


ANGINA = __ANGINA()


class __HF_IHD(NamedTuple):
    CSMR: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.cause_specific_mortality_rate',
        f'cause.{mod.HF_IHD_MODEL_NAME}.cause_specific_mortality_rate',
    )
    RESTRICTIONS: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.restrictions', f'cause.{mod.HF_IHD_MODEL_NAME}.restrictions'
    )
    PREVALENCE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.prevalence', f'cause.{mod.HF_IHD_MODEL_NAME}.prevalence'
    )
    INCIDENCE: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.incidence_rate', f'cause.{mod.HF_IHD_MODEL_NAME}.incidence_rate'
    )
    EMR: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.excess_mortality_rate',
        f'cause.{mod.HF_IHD_MODEL_NAME}.excess_mortality_rate',
    )
    DW: SourceSink = SourceSink(
        'cause.ischemic_heart_disease.disability_weight', f'cause.{mod.HF_IHD_MODEL_NAME}.disability_weight'
    )

    @property
    def name(self):
        return mod.HF_IHD_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


HF_IHD = __HF_IHD()


class __IschemicStroke(NamedTuple):
    CSMR: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.restrictions'
    INCIDENCE_ACUTE: str = f'cause.{mod.ISCHEMIC_STROKE_MODEL_NAME}.incidence_rate'

    PREVALENCE_ACUTE: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.prevalence'
    PREVALENCE_CHRONIC: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.prevalence'

    EMR_ACUTE: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'
    EMR_CHRONIC: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.excess_mortality_rate'

    DW_ACUTE: str = f'sequela.{mod.ACUTE_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'
    DW_CHRONIC: str = f'sequela.{mod.CHRONIC_ISCHEMIC_STROKE_STATE_NAME}.disability_weight'

    @property
    def name(self):
        return mod.ISCHEMIC_STROKE_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


ISCHEMIC_STROKE = __IschemicStroke()


class __PeripheralArterialDisease(NamedTuple):
    CSMR: str = f'cause.{mod.PAD_MODEL_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS: str = f'cause.{mod.PAD_MODEL_NAME}.restrictions'
    INCIDENCE: str = f'cause.{mod.PAD_MODEL_NAME}.incidence_rate'
    PREVALENCE: str = f'cause.{mod.PAD_MODEL_NAME}.prevalence'
    EMR: str = f'cause.{mod.PAD_MODEL_NAME}.excess_mortality_rate'
    DW: str = f'cause.{mod.PAD_MODEL_NAME}.disability_weight'

    @property
    def name(self):
        return mod.PAD_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


PAD = __PeripheralArterialDisease()


class __AtrialFibrillation(NamedTuple):
    CSMR: str = f'cause.{mod.AFIB_MODEL_NAME}.cause_specific_mortality_rate'
    RESTRICTIONS: str = f'cause.{mod.AFIB_MODEL_NAME}.restrictions'
    INCIDENCE: str = f'cause.{mod.AFIB_MODEL_NAME}.incidence_rate'
    PREVALENCE: str = f'cause.{mod.AFIB_MODEL_NAME}.prevalence'
    EMR: str = f'cause.{mod.AFIB_MODEL_NAME}.excess_mortality_rate'
    DW: str = f'cause.{mod.AFIB_MODEL_NAME}.disability_weight'

    @property
    def name(self):
        return mod.AFIB_MODEL_NAME

    @property
    def log_name(self):
        return self.name.replace('_', ' ')


AFIB = __AtrialFibrillation()


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
    MI,
    ANGINA,
    HF_IHD,
    # ISCHEMIC_STROKE,
    # PAD,
    # AFIB,
    # LDL_C,
    # SBP,
    # BMI,
    # FPG,
]
