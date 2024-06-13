from PIL import Image, ImageDraw
from pil_utils import BuildImage
from pil_utils.fonts import Font


def charPic(img: Image) -> Image:
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    num = len(str_map)
    font = Font.find("Consolas").load_font(15)
    img = BuildImage(img)
    img = img.convert("L").resize_width(150)
    img = img.resize((img.width, img.height // 2))
    lines = []
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            gray = img.image.getpixel((x, y))
            line += str_map[int(num * gray / 256)] if gray != 0 else " "
        lines.append(line)
    text = "\n".join(lines)
    text_img = Image.new("RGB", (2000, 2000), "white")
    draw = ImageDraw.Draw(text_img)
    _, _, w, h = draw.multiline_textbbox((0, 0), text, font=font)
    draw.multiline_text((0, 0), text, font=font, fill="black")
    text_img = text_img.crop((0, 0, w, h))
    return BuildImage(text_img).image
