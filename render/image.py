import random
import uuid

from PIL import Image, ImageFont, ImageDraw

from render.emoji_mapping import replace_emojis, split_str_and_emojis

NUM_IMAGES = 11
FONT_SIZE = 28
X_ORIGIN_TEXT = 55
Y_ORIGIN_TEXT = 130
VERTICAL_LINE_PADDING = 16
TEXT_HEIGHT = 23
MAXIMUM_NUMBER_OF_CHARACTERS = 224
CARD_TEXT_WIDTH = 350


def wrap_text(text, width, font):
    text_lines = []
    text_line = []
    text = text.replace('\n', ' [br] ')
    words = split_str_and_emojis(text)

    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w = font.getlength(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        text_lines.append(' '.join(text_line))

    return text_lines


def create_card(text):
    text = replace_emojis(text)
    message = (text[:MAXIMUM_NUMBER_OF_CHARACTERS] + ' ...') if len(text) > MAXIMUM_NUMBER_OF_CHARACTERS else text
    # TODO: look into https://github.com/googlefonts/nototools/blob/main/nototools/merge_fonts.py, try to use NotoColor
    font_path = 'fonts/NotoEmoji+IndieFlower.ttf'
    image = random.randint(1, NUM_IMAGES)
    x = Image.open(f'images/Group {image}.png').convert('RGB')
    font = ImageFont.truetype(font_path, FONT_SIZE, encoding='unic')
    lines = wrap_text(message, CARD_TEXT_WIDTH, font)
    draw = ImageDraw.Draw(x)
    y_offset = Y_ORIGIN_TEXT
    for line in lines:
        draw.text((X_ORIGIN_TEXT, y_offset), line, font=font, fill=(0, 0, 0), embedded_color=True)
        y_offset += TEXT_HEIGHT + VERTICAL_LINE_PADDING
    filename = f"/tmp/{uuid.uuid4()}.png"
    x.save(filename)
    return filename
