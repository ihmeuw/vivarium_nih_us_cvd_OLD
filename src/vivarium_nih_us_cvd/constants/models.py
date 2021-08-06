class TransitionString(str):

    def __new__(cls, value):
        # noinspection PyArgumentList
        obj = str.__new__(cls, value.lower())
        obj.from_state, obj.to_state = value.split('_TO_')
        return obj


###########################
# Disease Model variables #
###########################

IHD_MODEL_NAME = 'ischemic_heart_disease'
IHD_SUSCEPTIBLE_STATE_NAME = f'susceptible_to_{IHD_MODEL_NAME}'
ACUTE_MI_STATE_NAME = 'acute_myocardial_infarction'
POST_MI_STATE_NAME = 'post_myocardial_infarction'
IHD_MODEL_STATES = (IHD_SUSCEPTIBLE_STATE_NAME, ACUTE_MI_STATE_NAME, POST_MI_STATE_NAME)
IHD_MODEL_TRANSITIONS = (
    TransitionString(f'{IHD_SUSCEPTIBLE_STATE_NAME}_TO_{ACUTE_MI_STATE_NAME}'),
    TransitionString(f'{ACUTE_MI_STATE_NAME}_TO_{POST_MI_STATE_NAME}'),
    TransitionString(f'{POST_MI_STATE_NAME}_TO_{ACUTE_MI_STATE_NAME}'),
)

ISCHEMIC_STROKE_MODEL_NAME = 'ischemic_stroke'
ISCHEMIC_STROKE_SUSCEPTIBLE_STATE_NAME = f'susceptible_to_{ISCHEMIC_STROKE_MODEL_NAME}'
ACUTE_ISCHEMIC_STROKE_STATE_NAME = 'acute_ischemic_stroke'
CHRONIC_ISCHEMIC_STROKE_STATE_NAME = 'chronic_ischemic_stroke'
ISCHEMIC_STROKE_MODEL_STATES = (
    ISCHEMIC_STROKE_SUSCEPTIBLE_STATE_NAME,
    ACUTE_ISCHEMIC_STROKE_STATE_NAME,
    CHRONIC_ISCHEMIC_STROKE_STATE_NAME
)
ISCHEMIC_STROKE_MODEL_TRANSITIONS = (
    TransitionString(f'{ISCHEMIC_STROKE_SUSCEPTIBLE_STATE_NAME}_TO_{ACUTE_ISCHEMIC_STROKE_STATE_NAME}'),
    TransitionString(f'{ACUTE_ISCHEMIC_STROKE_STATE_NAME}_TO_{CHRONIC_ISCHEMIC_STROKE_STATE_NAME}'),
    TransitionString(f'{CHRONIC_ISCHEMIC_STROKE_STATE_NAME}_TO_{ACUTE_ISCHEMIC_STROKE_STATE_NAME}')
)

ANGINA_MODEL_NAME = 'angina'
ANGINA_SUSCEPTIBLE_STATE_NAME = f'susceptible_to_{ANGINA_MODEL_NAME}'
ANGINA_MODEL_STATES = (ANGINA_SUSCEPTIBLE_STATE_NAME, ANGINA_MODEL_NAME)
ANGINA_MODEL_TRANSITIONS = (
    TransitionString(f'{ANGINA_SUSCEPTIBLE_STATE_NAME}_TO_{ANGINA_MODEL_NAME}'),
)

PAD_MODEL_NAME = 'peripheral_artery_disease'
PAD_SUSCEPTIBLE_STATE_NAME = f'susceptible_to_{PAD_MODEL_NAME}'
PAD_MODEL_STATES = (PAD_SUSCEPTIBLE_STATE_NAME, PAD_MODEL_NAME)
PAD_MODEL_TRANSITIONS = (
    TransitionString(f'{PAD_SUSCEPTIBLE_STATE_NAME}_TO_{PAD_MODEL_NAME}'),
)

AFIB_MODEL_NAME = 'atrial_fibrillation_and_flutter'
AFIB_SUSCEPTIBLE_STATE_NAME = f'susceptible_to_{AFIB_MODEL_NAME}'
AFIB_MODEL_STATES = (AFIB_SUSCEPTIBLE_STATE_NAME, AFIB_MODEL_NAME)
AFIB_MODEL_TRANSITIONS = (
    TransitionString(f'{AFIB_SUSCEPTIBLE_STATE_NAME}_TO_{AFIB_MODEL_NAME}'),
)

STATE_MACHINE_MAP = {
    IHD_MODEL_NAME: {
        'states': IHD_MODEL_STATES,
        'transitions': IHD_MODEL_TRANSITIONS,
    },
    ISCHEMIC_STROKE_MODEL_NAME: {
        'states': ISCHEMIC_STROKE_MODEL_STATES,
        'transitions': ISCHEMIC_STROKE_MODEL_TRANSITIONS,
    },
    ANGINA_MODEL_NAME: {
        'states': ANGINA_MODEL_STATES,
        'transitions': ANGINA_MODEL_TRANSITIONS,
    },
}


STATES = tuple(state for model in STATE_MACHINE_MAP.values() for state in model['states'])
TRANSITIONS = tuple(state for model in STATE_MACHINE_MAP.values() for state in model['transitions'])
