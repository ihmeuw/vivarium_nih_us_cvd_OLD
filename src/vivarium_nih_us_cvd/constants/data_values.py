from datetime import datetime
from typing import NamedTuple


############################
# Disease Model Parameters #
############################
THRESHOLD_HIGH_SBP = 140
THRESHOLD_HIGH_LDLC = 5
THRESHOLD_HIGH_FPG = 7
THRESHOLD_HIGH_BMI = 25
THRESHOLD_LOW_BMI = 20


##############################
# Screening Model Parameters #
##############################

PROBABILITY_ATTENDING_SCREENING_KEY = 'probability_attending_screening'
PROBABILITY_ATTENDING_SCREENING_START_MEAN = 0.25
PROBABILITY_ATTENDING_SCREENING_START_STDDEV = 0.0025
PROBABILITY_ATTENDING_SCREENING_END_MEAN = 0.5
PROBABILITY_ATTENDING_SCREENING_END_STDDEV = 0.005

FIRST_SCREENING_AGE = 21
MID_SCREENING_AGE = 30
LAST_SCREENING_AGE = 65


###################################
# Scale-up Intervention Constants #
###################################
SCALE_UP_START_DT = datetime(2021, 1, 1)
SCALE_UP_END_DT = datetime(2030, 1, 1)
SCREENING_SCALE_UP_GOAL_COVERAGE = 0.50
SCREENING_SCALE_UP_DIFFERENCE = SCREENING_SCALE_UP_GOAL_COVERAGE - PROBABILITY_ATTENDING_SCREENING_START_MEAN

############################
# Stratification Constants #
############################

# Risk Categories
HIGH_RISK = 'high'
LOW_RISK = 'low'

RISK_CATEGORIES = [HIGH_RISK, LOW_RISK]

# ACS Categories
POST_CVE = 'post'
NO_CVE = 'none'

class __RiskGroups(NamedTuple):
    SBP_high_LDL_high_ACS_post: str = 'SBP_high_LDL_high_ACS_post'
    SBP_high_LDL_high_ACS_none: str = 'SBP_high_LDL_high_ACS_none'

    SBP_low_LDL_high_ACS_post: str = 'SBP_low_LDL_high_ACS_post'
    SBP_low_LDL_high_ACS_none: str = 'SBP_low_LDL_high_ACS_none'

    SBP_high_LDL_low_ACS_post: str = 'SBP_high_LDL_low_ACS_post'
    SBP_high_LDL_low_ACS_none: str = 'SBP_high_LDL_low_ACS_none'

    SBP_low_LDL_low_ACS_post: str = 'SBP_low_LDL_low_ACS_post'
    SBP_low_LDL_low_ACS_none: str = 'SBP_low_LDL_low_ACS_none'

RISK_GROUPS = __RiskGroups()
