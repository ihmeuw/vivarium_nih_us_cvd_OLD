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
from typing import Dict, Tuple, List

from gbd_mapping import causes, covariates, risk_factors, Sequela, ModelableEntity
from vivarium.framework.artifact import EntityKey
from vivarium.framework.artifact.artifact import Artifact
from vivarium_gbd_access import gbd
from vivarium_inputs import globals as vi_globals, interface, utilities as vi_utils, utility_data
from vivarium_inputs.mapping_extension import alternative_risk_factors

from vivarium_nih_us_cvd.constants import data_keys, models


def get_measure_wrapped(entity: ModelableEntity, key: str, location: str) -> pd.DataFrame:
    '''
    All calls to get_measure() need to have the location dropped. For the time being,
    simply use this function.
    '''
    return interface.get_measure(entity, key, location).droplevel('location')


def get_data(lookup_key: str, location: str) -> pd.DataFrame:
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

        data_keys.IHD.MI_ACUTE_PREV: load_ihd_prevalence,
        data_keys.IHD.MI_POST_PREV: load_ihd_prevalence,
        data_keys.IHD.ANGINA_PREV: load_ihd_prevalence,

        data_keys.IHD.MI_ACUTE_INCIDENCE: load_ihd_incidence,
        data_keys.IHD.MI_POST_INCIDENCE: load_ihd_incidence,
        data_keys.IHD.ANGINA_INCIDENCE: load_ihd_incidence,

        data_keys.IHD.MI_ACUTE_DW: load_ihd_disability_weight,
        data_keys.IHD.MI_POST_DW: load_ihd_disability_weight,
        data_keys.IHD.ANGINA_DW: load_ihd_disability_weight,

        data_keys.IHD.MI_ACUTE_EMR: load_ihd_emr,
        data_keys.IHD.MI_POST_EMR: load_ihd_emr,
        data_keys.IHD.ANGINA_EMR: load_ihd_emr,
        data_keys.IHD.CSMR: load_standard_data,
        data_keys.IHD.RESTRICTIONS: load_metadata,

        data_keys.ISCHEMIC_STROKE.ACUTE_PREV: load_ischemic_stroke_prevalence,
        data_keys.ISCHEMIC_STROKE.CHRONIC_PREV: load_ischemic_stroke_prevalence,

        data_keys.ISCHEMIC_STROKE.ACUTE_DW: load_ischemic_stroke_disability_weight,
        data_keys.ISCHEMIC_STROKE.CHRONIC_DW: load_ischemic_stroke_disability_weight,

        data_keys.ISCHEMIC_STROKE.ACUTE_EMR: load_ischemic_stroke_emr,
        data_keys.ISCHEMIC_STROKE.CHRONIC_EMR: load_ischemic_stroke_emr,
        data_keys.ISCHEMIC_STROKE.ACUTE_INCIDENCE: load_standard_data,
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
    return mapping[lookup_key](lookup_key, location)


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
def get_prevalence_weighted_disability_weight(sequelae: List[Sequela], location: str) -> List[pd.DataFrame]:
    prevalence_disability_weights = []
    for s in sequelae:
        prevalence = get_measure_wrapped(s, 'prevalence', location)
        disability_weight = get_measure_wrapped(s, 'disability_weight', location)
        prevalence_disability_weights.append(prevalence * disability_weight)
    return prevalence_disability_weights


def get_ihd_sequelae() -> Tuple[List[Sequela], List[Sequela], List[Sequela]]:
    acute_mi_sequelae = [s for s in causes.ischemic_heart_disease.sequelae if 'acute' in s.name]
    post_mi_sequelae = [s for s in causes.ischemic_heart_disease.sequelae if 'ischemic_heart_disease' in s.name]
    angina_mi_sequelae = [s for s in causes.ischemic_heart_disease.sequelae if 'angina' in s.name]
    return acute_mi_sequelae, post_mi_sequelae, angina_mi_sequelae


def load_ihd_prevalence(key: str, location: str) -> pd.DataFrame:
    acute_mi_sequelae, post_mi_sequelae, angina_mi_sequelae = get_ihd_sequelae()
    map = {
        data_keys.IHD.MI_ACUTE_PREV: acute_mi_sequelae,
        data_keys.IHD.MI_POST_PREV: post_mi_sequelae,
        data_keys.IHD.ANGINA_PREV: angina_mi_sequelae,
    }
    prevalence = sum(get_measure_wrapped(s, 'prevalence', location) for s in map[key])
    return prevalence


def load_ihd_incidence(key: str, location: str) -> pd.DataFrame:
    map = {
        data_keys.IHD.MI_ACUTE_INCIDENCE: 24694,
        data_keys.IHD.MI_POST_INCIDENCE: 24694,
        data_keys.IHD.ANGINA_INCIDENCE: 1817,
    }
    #ihd_all = get_measure_wrapped(causes.ischemic_heart_disease, 'prevalence', location)
    ihd_prev_this = _load_em_from_meid(map[key], 'Prevalence', location)
    ihd_this = _load_em_from_meid(map[key], 'Incidence rate', location)
    return ihd_this / (1 - ihd_prev_this)


def load_ihd_disability_weight(key: str, location: str) -> pd.DataFrame:
    acute_mi_sequelae, post_mi_sequelae, angina_mi_sequelae = get_ihd_sequelae()
    map = {
        data_keys.IHD.MI_ACUTE_DW: acute_mi_sequelae,
        data_keys.IHD.MI_POST_DW: post_mi_sequelae,
        data_keys.IHD.ANGINA_DW: angina_mi_sequelae,
    }
    prevalence_disability_weights = get_prevalence_weighted_disability_weight(map[key], location)
    ihd_prevalence = get_measure_wrapped(causes.ischemic_heart_disease, 'prevalence', location)
    ihd_disability_weight = (sum(prevalence_disability_weights) / ihd_prevalence).fillna(0)
    return ihd_disability_weight


def load_ihd_emr(key: str, location: str) -> pd.DataFrame:
    map = {
        data_keys.IHD.MI_ACUTE_EMR: 24694,
        data_keys.IHD.MI_POST_EMR: 15755,
        data_keys.IHD.ANGINA_EMR: 1817,
    }
    return _load_em_from_meid(map[key], 'Excess mortality rate', location)


def get_ischemic_stroke_sequelae() ->  Tuple[pd.DataFrame, pd.DataFrame]:
    acute_sequelae = [s for s in causes.ischemic_stroke.sequelae if 'acute' in s.name]
    chronic_sequelae = [s for s in causes.ischemic_stroke.sequelae if 'chronic' in s.name]
    return acute_sequelae, chronic_sequelae


def load_ischemic_stroke_prevalence(key: str, location: str) -> pd.DataFrame:
    acute_sequelae, chronic_sequelae = get_ischemic_stroke_sequelae()
    map = {
        data_keys.ISCHEMIC_STROKE.ACUTE_PREV: acute_sequelae,
        data_keys.ISCHEMIC_STROKE.CHRONIC_PREV: chronic_sequelae
    }
    prevalence = sum(get_measure_wrapped(s, 'prevalence', location) for s in map[key])
    return prevalence


def load_ischemic_stroke_disability_weight(key: str, location: str) -> pd.DataFrame:
    acute_sequelae, chronic_sequelae = get_ischemic_stroke_sequelae()
    map = {
        data_keys.ISCHEMIC_STROKE.ACUTE_DW: acute_sequelae,
        data_keys.ISCHEMIC_STROKE.CHRONIC_DW: chronic_sequelae
    }
    prevalence_disability_weights = get_prevalence_weighted_disability_weight(map[key], location)
    ischemic_stroke_prevalence = get_measure_wrapped(causes.ischemic_stroke, 'prevalence', location)
    ischemic_stroke_disability_weight = (sum(prevalence_disability_weights) / ischemic_stroke_prevalence).fillna(0)
    return ischemic_stroke_disability_weight


def load_ischemic_stroke_emr(key: str, location: str) -> pd.DataFrame:
    map = {
        data_keys.ISCHEMIC_STROKE.ACUTE_EMR: 24714,
        data_keys.ISCHEMIC_STROKE.CHRONIC_EMR: 10837,
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
    artifact.write(data_keys.IHD.RESTRICTIONS_ANGINA, artifact.load(data_keys.IHD.RESTRICTIONS))
    # Maybe use later... For now use IHD cause_specific_mortality, which contains angina emr,
    #   and make angina csmr be zero. The csmr is necessary to use the default SI model for angina
    # csmr_angina = (load_ihd_prevalence(data_keys.IHD.ANGINA_PREV, location)
    #               * load_ihd_emr(data_keys.IHD.ANGINA_EMR, location))
    draws = [f'draw_{i}' for i in range(1000)]
    df_zeros = load_ihd_emr(data_keys.IHD.ANGINA_EMR, location)
    df_zeros[draws] = 0.0
    artifact.write(data_keys.IHD.CSMR_ANGINA, df_zeros)


    # Need to make RR data match causes in the model
    map = {
        'ischemic_heart_disease': ['acute_myocardial_infarction', 'post_myocardial_infarction_to_acute_myocardial_infarction'],
        'ischemic_stroke': ['acute_ischemic_stroke', 'chronic_ischemic_stroke_to_acute_ischemic_stroke'],
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
