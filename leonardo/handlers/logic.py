from config.constants import QUOTE_FREQUENCY, MENTION_FREQUENCY, GO_ALIASES
import random

def should_include_quote(counter):
    return counter % QUOTE_FREQUENCY == 0

def should_use_direct_mention(counter):
    return counter % MENTION_FREQUENCY == 0

def get_go_synonym():
    return random.choice(GO_ALIASES)
