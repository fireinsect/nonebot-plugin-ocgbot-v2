import re
import httpx
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event, Bot, Message, MessageSegment
from nonebot import on_command

from nonebot_plugin_ocgbot_v2.libraries.image import image_to_base64, text_to_image_with_back

gradeUrl = "https://api.jihuanshe.com/api/market/search/match-product?game_key=ygo&game_sub_key=ocg&type=card_version"

priceSearch = on_command('集换社查询', aliases={'价格查询', '查价格', '查询价格', '查卡价'})


@priceSearch.handle()
async def _(bot: Bot, event: Event, state: T_State,args: Message = CommandArg()):
    regex = "(.+) (page)?([0-9]+)?"
    text = str(args).strip()
    search_group = re.match(regex, text)
    try:
        print(search_group.groups()[2])
    except Exception as e:
        text = text + " 1"
        search_group = re.match(regex, str(text))
    try:
        if search_group.groups()[2] is None:
            text = text + " 1"
            search_group = re.match(regex, str(text))
        page = search_group.groups()[2]
        textNext = search_group.groups()[0]
        name = textNext
        url = f"{gradeUrl}&keyword={name}&page={page}"
        result = httpx.get(url).json()
        page_text = f"找到了{result['total']}条数据哟~,当前{result['current_page']}/{result['last_page']}页 数据来源：集换社"

        await priceSearch.send(Message([
            MessageSegment("image", {
                "file": f"base64://{str(image_to_base64(text_to_image_with_back(getPriceStr(result), page_text, '价格表')), encoding='utf-8')}"
            })]))
    except Exception as e:
        e.with_traceback()
        await priceSearch.finish("咿呀？查询失败了呢")


def getPriceStr(json):
    result = ""
    for item in json['data']:
        result += f"{item['number']} {item['rarity']}   {item['min_price']}￥起 \n名称：{item['name_cn']} {item['name_origin']} \n\n"
    return result
