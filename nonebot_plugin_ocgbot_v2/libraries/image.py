import base64
from io import BytesIO
from pathlib import Path

from PIL import ImageFont, ImageDraw, Image
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import font_path, image_path

fontpath = str(Path(font_path) / "msyh.ttc")
background = Image.open(Path(image_path) / "background.png")


def draw_text(img_pil, text, offset_x):
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(fontpath, 48)
    width, height = draw.textsize(text, font)
    x = 5
    if width > 390:
        font = ImageFont.truetype(fontpath, int(390 * 48 / width))
        width, height = draw.textsize(text, font)
    else:
        x = int((400 - width) / 2)
    draw.rectangle((x + offset_x - 2, 360, x + 2 + width + offset_x, 360 + height * 1.2), fill=(0, 0, 0, 255))
    draw.text((x + offset_x, 360), text, font=font, fill=(255, 255, 255, 255))


def text_to_image(text):
    font = ImageFont.truetype(fontpath, 24)
    padding = 15
    margin = 10
    text_list = text.split('\n')
    max_width = 0
    for text in text_list:
        w, h = getsize(font, text)
        max_width = max(max_width, w)
    wa = max_width + padding * 2
    ha = h * len(text_list) + margin * (len(text_list) - 1) + padding * 2
    i = Image.new('RGB', (wa, ha), color=(255, 255, 255))
    draw = ImageDraw.Draw(i)
    for j in range(len(text_list)):
        text = text_list[j]
        draw.text((padding, padding + j * (margin + h)), text, font=font, fill=(0, 0, 0))
    return i


def text_to_image2(text, page_text):
    font = ImageFont.truetype(fontpath, 28)
    font_page = ImageFont.truetype(fontpath, 30)
    padding = 30
    margin = 33
    text_list = text.split('\n')
    max_width = font.getbbox(page_text)[0]
    for text in text_list:
        w, h = getsize(font, text)
        max_width = max(max_width, w)
    wa = max_width + padding * 2 + 100
    ha = h * len(text_list) + h + margin * (len(text_list)) + padding * 2
    # i = Image.new('RGB', (wa, ha), color=(255, 255, 255))
    i = background
    change = max(ha / i.height, wa / i.width)
    i = i.resize((int(i.width * change), int(i.height * change)), Image.LANCZOS)
    i = i.crop(
        (int(i.width / 2 - wa / 2), int(i.height / 2 - ha / 2), int(i.width / 2 + wa / 2), int(i.height / 2 + ha / 2)))
    draw = ImageDraw.Draw(i)
    for j in range(len(text_list)):
        text = text_list[j]
        draw.text((padding, padding + j * (margin + h)), text, font=font, fill=(0, 0, 0))
    draw.text((padding, padding + j * (margin + h)), page_text, font=font_page, fill=(0, 0, 0))
    return i


def text_to_image_with_back(text, page_text, title):
    font = ImageFont.truetype(fontpath, 28)
    font_title = ImageFont.truetype(str(Path(font_path) / "qmzl.ttf"), 50)
    font_page = ImageFont.truetype(fontpath, 30)
    padding = 30
    margin = 33
    text_list = text.split('\n')
    max_width = 0
    title_w, title_h = getsize(font_title, title)
    for text in text_list:
        w, h = getsize(font, text)
        max_width = max(max_width, w)
    max_width = max(max_width, font.getlength(page_text))
    max_width = max(max_width, title_w)
    wa = max_width + padding * 2 + 100
    ha = h * len(text_list) + h + margin * (len(text_list)) + padding * 2 + title_h + int(title_h * 0.8)
    i = background
    change = max(ha / i.height, wa / i.width)
    i = i.resize((int(i.width * change), int(i.height * change)), Image.LANCZOS)
    i = i.crop(
        (int(i.width / 2 - wa / 2), int(i.height / 2 - ha / 2), int(i.width / 2 + wa / 2), int(i.height / 2 + ha / 2)))
    draw = ImageDraw.Draw(i)
    draw.text((int(i.width / 2 - title_w / 2), padding), title, font=font_title, fill=(0, 0, 0))
    for j in range(len(text_list)):
        text = text_list[j]
        draw.text((padding, padding + j * (margin + h) + margin + title_h), text, font=font, fill=(0, 0, 0))
    draw.text((padding, padding + j * (margin + h) + margin + title_h), page_text, font=font_page, fill=(0, 0, 0))
    return i


def image_to_base64(img, format='PNG'):
    output_buffer = BytesIO()
    img.save(output_buffer, format)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


def getsize(font, text):
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom - top
