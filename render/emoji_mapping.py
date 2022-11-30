import re
from functools import reduce
from operator import add
import json

EMOJI_CODES_LOOKUP = None


def load_lookup():
    with open("data/emoji.json", 'r') as emoji_mappings_file:
        return {
            e["short_name"]: e
            for e in json.load(emoji_mappings_file)
        }


def replace_emojis(text):
    global EMOJI_CODES_LOOKUP
    if EMOJI_CODES_LOOKUP is None:
        EMOJI_CODES_LOOKUP = load_lookup()

    emoji_regex = ":([a-zA-Z0-9-_+]+):(?::(skin-tone[a-zA-Z0-9-_+]+):)?"

    def replace(match):
        emoji = match.group(1)
        if emoji in EMOJI_CODES_LOOKUP:
            unified = EMOJI_CODES_LOOKUP[emoji]['unified']
            codes = [int(code, 16) for code in unified.split("-")]
            return reduce(add, (chr(code) for code in codes))
        else:
            return match.group()

    return re.sub(emoji_regex, replace, text)
