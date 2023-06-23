import random
import re
from io import BytesIO

import requests
from PIL import Image
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment

from nonebot_plugin_ocgbot_v2.libraries.globalMessage import image_path
from nonebot_plugin_ocgbot_v2.libraries.image import image_to_base64

juexing = on_command('mai觉醒')
jiaru = on_command('mai加入')
txApi = "https://q1.qlogo.cn/g?b=qq&s=5&nk="
juexing_url = image_path+"juexing.png"
jiaru_url = image_path+"jiaru.png"


@juexing.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qq = str(event.sender.user_id)
    image = Image.open(juexing_url)
    tx = Image.open(BytesIO(requests.get(txApi + qq).content))
    tx = tx.resize((510, 510))
    i = Image.new('RGB', image.size, color=(255, 255, 255))
    i.paste(tx, (int((i.size[0] - tx.size[0]) / 2), int((i.size[1] - tx.size[1]) / 2)))
    i.paste(image, (0,0),mask=image)
    await juexing.send([
        MessageSegment.image(f"base64://{str(image_to_base64(i), encoding='utf-8')}")
    ])

@jiaru.handle()
async def _(bot: Bot, event: Event, state: T_State):
    qq = str(event.sender.user_id)
    image = Image.open(jiaru_url)
    tx = Image.open(BytesIO(requests.get(txApi + qq).content))
    tx = tx.resize((515, 515))
    i = Image.new('RGB', image.size, color=(255, 255, 255))
    i.paste(tx, (int((i.size[0] - tx.size[0]) / 2), int((i.size[1] - tx.size[1]) / 2)))
    i.paste(image, (0,0),mask=image)
    await jiaru.send([
        MessageSegment.image(f"base64://{str(image_to_base64(i), encoding='utf-8')}")
    ])