import asyncio
import json
import os.path
from threading import Thread

import httpx
from nonebot import logger, get_driver
from nonebot_plugin_ocgbot_v2.libraries.forbideGet import forbiddenGet
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import json_path, pics_path, static_path_abso, deck_path
from nonebot_plugin_ocgbot_v2.libraries.staticvar import nick_name_0, nick_name_1, forbidden, daily_card
from nonebot.plugin import PluginMetadata
import nonebot_plugin_ocgbot_v2.data_update
import nonebot_plugin_ocgbot_v2.ocg
import nonebot_plugin_ocgbot_v2.guess_card
import nonebot_plugin_ocgbot_v2.help
import nonebot_plugin_ocgbot_v2.daily
import nonebot_plugin_ocgbot_v2.cardPieChart
import nonebot_plugin_ocgbot_v2.priceSearch
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonbot-plugin-ocgbot-v2",
    description="提供游戏王相关服务",
    usage="提供包括查卡、随机抽卡、猜卡等功能",

    type="application",

    homepage="https://github.com/fireinsect/nonebot-plugin-ocgbot-v2/",

    config=Config,

    supported_adapters={"~onebot.v11"},
)

deck_url = "https://gitee.com/fireinsect/image-save/raw/master/decks/"


class NetworkError(Exception):
    pass


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise NetworkError(f"{url} 下载失败！")


def saveImg(wj_path: str, img: bytes):
    with open(wj_path, "wb") as f:  # 文件写入
        f.write(img)


async def download(wjs_path, wj, deck):
    wj_path = wjs_path + "/" + wj
    if not os.path.exists(wj_path):
        byte = await download_url(deck_url + "{0}/{1}".format(deck, wj))
        saveImg(wj_path, byte)
        logger.info("图片{0}下载成功".format(wj))


def deckDownload():
    deck_json = deck_path + "deck_list.json"
    if not os.path.exists(deck_json):
        return
    with open(deck_json, 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
    for deck in js['list']:
        wjs_path = deck_path + deck
        if not os.path.exists(wjs_path):
            logger.info("文件夹decks/" + deck + " 不存在，已经创建")
            os.mkdir(wjs_path)
        for wj in js['list'][deck]:
            asyncio.run(download(wjs_path, wj, deck))


async def nickNameInit():
    nick_path = json_path + "nickname.json"
    try:
        # 尝试读取
        with open(nick_path, 'r', encoding='utf-8') as f:
            nick_json = json.loads(f.read())['RECORDS']
            logger.info(f'nickname.json 读取成功')
            for js in nick_json:
                if js['NK_type'] == 0:
                    nick_name_0.append(js)
                if js['NK_type'] == 1:
                    nick_name_1.append(js)
    except Exception as e:
        # 读取失败
        logger.warning(f'nickname.json 读取失败')


async def forbideInit():
    forbide_path = json_path + "forbidden.json"
    try:
        # 尝试读取
        with open(forbide_path, 'r', encoding='utf-8') as f:
            forbidden_json = json.loads(f.read())
            logger.info(f'forbidden.json 读取成功')
            for js in forbidden_json:
                forbidden.append(js)
    except Exception as e:
        # 读取失败
        logger.warning(f'forbidden.json 读取失败,正在获取禁卡表')
        forbiddenGet()


async def dailyInit():
    nick_path = json_path + "daily_card.json"
    try:
        # 尝试读取
        with open(nick_path, 'r', encoding='utf-8') as f:
            daily_json = json.loads(f.read())
            logger.info(f'daily_card.json 读取成功')
            for daily in daily_json:
                daily_card.append(daily)
    except Exception as e:
        # 读取失败
        logger.warning(f'daily_card.json 读取失败')


async def init():
    logger.info("开始初始化")
    if not os.path.exists(pics_path):
        logger.info("未发现图片文件夹，已经创建")
        os.mkdir(pics_path + "pics")
    thread01 = Thread(target=deckDownload)
    thread01.start()
    await nickNameInit()
    await forbideInit()
    await dailyInit()


driver = get_driver()
driver.on_startup(init)
