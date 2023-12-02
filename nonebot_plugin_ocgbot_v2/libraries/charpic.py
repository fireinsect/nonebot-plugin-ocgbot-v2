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
            line += str_map[int(num * gray / 256)]
        lines.append(line)
    text = "\n".join(lines)
    w, h = font.getsize_multiline(text)
    text_img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(text_img)
    draw.multiline_text((0, 0), text, font=font, fill="black")
    return BuildImage(text_img).image
