from PIL import ImageFont
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import font_path

font = font_path + "qmzl.ttf"
fontWeek, fontList, fontCardStr, fontText, fontPoint = None, None, None, None, None


def font_init():
    global fontWeek, fontList, fontCardStr, fontText, fontPoint
    # 星期显示字体
    fontWeek = ImageFont.truetype(font, 45)
    # 宜忌显示字体
    fontList = ImageFont.truetype(font, 30)
    # 卡牌信息字体
    fontCardStr = ImageFont.truetype(font, 40)
    # 小贴士字体
    fontText = ImageFont.truetype(font, 28)
    # 点数字体
    fontPoint = ImageFont.truetype(font, 60)
