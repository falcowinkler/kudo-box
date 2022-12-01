import json
import os
import re
from functools import reduce
from operator import add, concat


def load_lookup():
    # data is official from slack: https://github.com/iamcal/emoji-data
    with open("data/emoji.json", 'r') as emoji_mappings_file:
        d = {
            short_name: e
            for e in json.load(emoji_mappings_file)
            for short_name in e["short_names"]
        }
        d["pride"] = d["rainbow-flag"]
        return d


EMOJI_CODES_LOOKUP = load_lookup()


def to_unicode(unified):
    codes = [int(code, 16) for code in unified.split("-")]
    return reduce(add, (chr(code) for code in codes))


def unicode_emoji_regexp():
    # Sort emoji by length to make sure multi-character emojis are
    # matched first
    emojis = sorted([to_unicode(e['unified']) for e in EMOJI_CODES_LOOKUP.values()], key=len)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    return re.compile(pattern)


def split_str_and_emojis(s):
    em_split_emoji = unicode_emoji_regexp().split(s)
    em_split_whitespace = [substr.split() for substr in em_split_emoji]
    em_split = reduce(concat, em_split_whitespace)
    return em_split


def replace_emojis(text, parse_skin_tones=False):
    # https://github.com/alexmick/emoji-data-python/blob/master/emoji_data_python/replacement.py
    emoji_regex = ":([a-zA-Z0-9-_+]+):(?::(skin-tone[2-6]+):)?"

    def replace(match):
        emoji = match.group(1).replace(":", "")
        if emoji.startswith("skin-tone") and not parse_skin_tones:  # TODO: skin tones disabled for now
            return ""
        if emoji in EMOJI_CODES_LOOKUP:

            base_emoji = EMOJI_CODES_LOOKUP[emoji]['unified']

            if match.lastindex == 2 and parse_skin_tones:  # TODO parse skin tones when color font works
                skin_tone_match = match.group(2).replace(":", "")
                skin_tone_modifier_code = EMOJI_CODES_LOOKUP[skin_tone_match]['unified']
                emoji_with_skin_tone = EMOJI_CODES_LOOKUP[emoji]["skin_variations"][skin_tone_modifier_code]
                if emoji_with_skin_tone is None:
                    return to_unicode(f"{base_emoji}{skin_tone_modifier_code}")
                return to_unicode(emoji_with_skin_tone['unified'])

            return to_unicode(base_emoji)
        else:
            return match.group()

    return re.sub(emoji_regex, replace, text)
