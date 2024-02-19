from pathlib import Path

from PIL import ImageFont
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import font_path

font = str(Path(font_path) / "qmzl.ttf")
fonts = {}


# fontWeek, fontList, fontCardStr, fontText, fontPoint = None, None, None, None, None


def font_init():
    # global fontWeek, fontList, fontCardStr, fontText, fontPoint
    # 星期显示字体
    fonts['fontWeek'] = ImageFont.truetype(font, 45)
    # 宜忌显示字体
    fonts['fontList'] = ImageFont.truetype(font, 30)
    # 卡牌信息字体
    fonts['fontCardStr'] = ImageFont.truetype(font, 40)
    # 小贴士字体
    fonts['fontText'] = ImageFont.truetype(font, 28)
    # 点数字体
    fonts['fontPoint'] = ImageFont.truetype(font, 60)
