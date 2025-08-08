quote_counter = 0
mention_counter = 0
used_quotes = set()

def can_quote():
    global quote_counter
    quote_counter += 1
    return quote_counter % 5 == 0

def can_mention_direct():
    global mention_counter
    mention_counter += 1
    return mention_counter % 10 == 0

def is_new_quote(quote):
    if quote in used_quotes:
        return False
    used_quotes.add(quote)
    return True
