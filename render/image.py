import json
import random
import textwrap
import uuid
import re
from functools import reduce
from operator import add

from PIL import Image, ImageFont, ImageDraw

NUM_IMAGES = 11
NUMBER_OF_CHARACTERS_BEFORE_CARRIER_RETURN = 20
FONT_SIZE = 28
X_ORIGIN_TEXT = 55
Y_ORIGIN_TEXT = 130
VERTICAL_LINE_PADDING = 16
TEXT_HEIGHT = 23
MAXIMUM_NUMBER_OF_CHARACTERS = 224

with open("data/emoji.json", 'r') as emoji_mappings_file:
    EMOJI_CODES_LOOKUP = {
        e["short_name"]: e
        for e in json.load(emoji_mappings_file)
    }


def replace_emojis(text):
    emoji_regex = ":([a-zA-Z0-9-_+]+):(?::([a-zA-Z0-9-_+]+):)?"

    def replace(match):
        emoji = match.group(1)
        if emoji in EMOJI_CODES_LOOKUP:
            unified = EMOJI_CODES_LOOKUP[emoji]['unified']
            codes = [int(code, 16) for code in unified.split("-")]
            return reduce(add, (chr(code) for code in codes))
        else:
            return emoji

    return re.sub(emoji_regex, replace, text)


def create_card(text):
    text = replace_emojis(text)
    message = (text[:MAXIMUM_NUMBER_OF_CHARACTERS] + ' ...') if len(text) > MAXIMUM_NUMBER_OF_CHARACTERS else text
    font_path = 'fonts/NotoEmoji+MostlyMono.ttf'
    image = random.randint(1, NUM_IMAGES)
    x = Image.open(f'images/Group {image}.png').convert('RGB')
    lines = textwrap.wrap(message, width=NUMBER_OF_CHARACTERS_BEFORE_CARRIER_RETURN)
    font = ImageFont.truetype(font_path, FONT_SIZE, encoding='unic')
    draw = ImageDraw.Draw(x)
    y_offset = Y_ORIGIN_TEXT
    for line in lines:
        draw.text((X_ORIGIN_TEXT, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += TEXT_HEIGHT + VERTICAL_LINE_PADDING
    filename = f"/tmp/{uuid.uuid4()}.png"
    x.save(filename)
    return filename


create_card("asdfsadfee :flag-bi:")
