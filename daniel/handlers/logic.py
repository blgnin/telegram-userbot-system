from config.constants import FLIRT_FREQ, AGGRO_FREQ, PUNCHLINE_FREQ
import random

def should_flirt(counter):
    return counter % FLIRT_FREQ == 0

def should_aggro(counter):
    return counter % AGGRO_FREQ == 0

def should_punchline(counter):
    return counter % PUNCHLINE_FREQ == 0
