import datetime
from pathlib import Path

from PIL import Image, ImageDraw
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.typing import T_State

from nonebot_plugin_ocgbot_v2.libraries.FontUtil import fonts
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import image_path, deck_path
from nonebot_plugin_ocgbot_v2.libraries.staticvar import daily_card
from nonebot_plugin_ocgbot_v2.libraries.tool import hash
from nonebot_plugin_ocgbot_v2.libraries.image import image_to_base64
from nonebot_plugin_ocgbot_v2.libraries.sendAction import card_txt

wm_list = ['同调', '仪式', '融合', '超量', '链接', '灵摆', '顶 G', '重坑', '干饭', '开壶', '唠嗑', '摸鱼', '说书',
           '开包', '懒觉', '锻炼', '口胡']
dailycard = on_command('今日游戏王', aliases={'今日卡运', '今日牌运'})
obj = daily_card
lend = len(wm_list)


@dailycard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 正常版本
    qq = int(event.get_user_id())
    point = int(hash(qq))
    wm_value = []
    for i in range(lend):
        wm_value.append(point & 3)
        point >>= 2
    await dailycard.finish(getDailyPic(point, wm_value), at_sender=True)


def getDailyPic(point: int, wm_value):
    card = obj[point % len(obj)]
    no = point % int(card['nums'])
    if card['type'] == "系列":
        back_pic = Image.open(Path(image_path) / "daily_xilie.png")
    else:
        back_pic = Image.open(Path(image_path) / "daily_kapai.png")
    url = Path(deck_path) / f"{card['id']}/{card['id']}-{no}.jpg"
    cardPic = Image.open(url)
    proper_list = []
    envy_list = []
    for i in range(lend):
        if wm_value[i] == 3:
            proper_list.append(wm_list[i])
        elif wm_value[i] == 0:
            envy_list.append(wm_list[i])
    weekday = datetime.datetime.now().weekday()
    daily = point % 100
    card_str = f"{card['name']}-{no + 1}"
    extra_text = "小蓝提醒您：打牌要保持良好心态哟~"
    pic_joint(back_pic, cardPic, daily, extra_text, weekday, card_str, proper_list, envy_list)
    return Message([
        MessageSegment("image",
                       {
                           "file": f"base64://{str(image_to_base64(back_pic), encoding='utf-8')}"
                       })])


def getDailyText(point: int, wm_value):
    daily = point % 100
    s = f"今日人品值：{daily}\n"
    flag = 0
    for i in range(lend):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}'
            if flag % 2 == 0:
                s += '　　'
                flag += 1
            else:
                s += f'\n'
                flag += 1
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}'
            if flag % 2 == 0:
                s += '　　'
                flag += 1
            else:
                s += f'\n'
                flag += 1
        if i == lend - 1 and flag % 2 == 1:
            s += f'\n'
    card = obj[point % len(obj)]
    s += f'小蓝提醒您：打牌要保持良好心态哟~\n今日{card["type"]}：'
    no = point % int(card['nums'])
    return Message([
                       MessageSegment("text", {"text": s})
                   ] + card_txt(card, no))


# ---图片拼接---


def pic_joint(backPic: Image, cardPic: Image, daily: int, extra_text: str, weekday: int, card_str: str, proper_list,
              envy_list):
    draw = ImageDraw.Draw(backPic)
    num_dict = {"0": u"一", "1": u"二", "2": u"三", "3": u"四", "4": u"五", "5": u"六", "6": u"日"}
    week = f"星期{num_dict.get(str(weekday))}"
    # 文字写入通过不同fill指定颜色
    # 写入星期
    draw.text((550, 50), week, font=fonts['fontWeek'], fill=(92, 128, 160))
    # 写入宜忌
    for i in range(len(proper_list)):
        if i > 5:
            break
        else:
            draw.text((60 + i % 3 * 102, 325 + int(i / 3) * 40), proper_list[i], font=fonts['fontList'], fill=(92, 128, 160))
    for i in range(len(envy_list)):
        if i > 5:
            break
        else:
            draw.text((60 + i % 3 * 102, 507 + int(i / 3) * 40), envy_list[i], font=fonts['fontList'], fill=(92, 128, 160))
    # 写入小贴士
    draw.text(((backPic.width - fonts['fontText'].size * len(extra_text)) / 2, 690), extra_text, font=fonts['fontText'],
              fill=(92, 128, 160))
    # 贴入卡图
    backPic.paste(cardPic.resize((280, 280)), (460, 290))
    # 写入卡牌信息
    draw.text((430 + (400 - fonts['fontCardStr'].size * len(card_str)) / 2, 580), card_str, font=fonts['fontCardStr'],
              fill=(92, 128, 160))
    # 写入点数
    draw.text((260, 200), str(daily), font=fonts['fontPoint'], fill=(92, 128, 160))
