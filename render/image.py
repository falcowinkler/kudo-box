import random
import textwrap
import uuid

from PIL import Image, ImageFont, ImageDraw

NUM_IMAGES = 11
NUMBER_OF_CHARACTERS_BEFORE_CARRIER_RETURN = 22
FONT_SIZE = 28
X_ORIGIN_TEXT = 30
Y_ORIGIN_TEXT = 130
VERTICAL_LINE_PADDING = 10
TEXT_HEIGHT = 22


def create_card(text):
    text = f"""{text}"""

    font_path = 'fonts/MostlyMono.ttf'
    image = random.randint(1, NUM_IMAGES)
    x = Image.open(f'images/{image}.png').convert('RGB')
    lines = textwrap.wrap(text, width=NUMBER_OF_CHARACTERS_BEFORE_CARRIER_RETURN)
    font = ImageFont.truetype(font_path, FONT_SIZE, encoding='unic')
    draw = ImageDraw.Draw(x)
    y_offset = Y_ORIGIN_TEXT
    for line in lines:
        draw.text((X_ORIGIN_TEXT, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += TEXT_HEIGHT + VERTICAL_LINE_PADDING
    filename = f"/tmp/{uuid.uuid4()}.png"
    x.save(filename)
    return filename
