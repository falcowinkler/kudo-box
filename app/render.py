import random
import textwrap
import uuid

from PIL import Image, ImageFont, ImageDraw

def create_card(text):
    text = f"""{text}"""

    font_path = 'fonts/MostlyMono.ttf'
    num_images = 11
    image = random.randint(1, num_images)
    x = Image.open(f'images/{image}.png').convert('RGB')
    lines = textwrap.wrap(text, width=22)
    font = ImageFont.truetype(font_path, 28, encoding='unic')
    y_text = 130
    line_padding = 10
    height = 22
    draw = ImageDraw.Draw(x)
    for line in lines:
        draw.text((30, y_text), line, font=font, fill=(0, 0, 0))
        y_text += height + line_padding
    filename = f"generated/{uuid.uuid4()}.png"
    x.save(filename)
    return filename