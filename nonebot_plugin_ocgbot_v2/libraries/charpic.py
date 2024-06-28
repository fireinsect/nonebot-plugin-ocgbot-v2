from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from  nonebot_plugin_ocgbot_v2.libraries.globalMessage import font_path

fontpath = str(Path(font_path) / "consola.ttf")
def charPic(img: Image) -> Image:
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    num = len(str_map)
    font = ImageFont.truetype(fontpath, 15)
    img = img.convert("L").resize((200, int(img.height * 200 / img.width)))
    img = img.resize((img.width, img.height // 2))
    lines = []
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            gray = img.getpixel((x, y))
            line += str_map[int(num * gray / 256)] if gray != 0 else " "
        lines.append(line)
    text = "\n".join(lines)
    text_img = Image.new("RGB", (2000, 2000), "white")
    draw = ImageDraw.Draw(text_img)
    _, _, w, h = draw.multiline_textbbox((0, 0), text, font=font)
    draw.multiline_text((0, 0), text, font=font, fill="black")
    text_img = text_img.crop((0, 0, w, h))
    return text_img
