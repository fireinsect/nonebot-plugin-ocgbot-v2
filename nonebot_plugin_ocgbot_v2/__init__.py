import asyncio
import json
import os.path
from pathlib import Path
from threading import Thread
import httpx
from nonebot import logger, get_driver
from nonebot_plugin_ocgbot_v2.libraries.forbideGet import forbiddenGet
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import json_path, pics_path, deck_path, font_path
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
    name="游戏王小蓝卡查",
    description="提供游戏王相关服务",
    usage="提供包括查卡、随机抽卡、猜卡等功能",

    type="application",

    homepage="https://github.com/fireinsect/nonebot-plugin-ocgbot-v2/",

    config=Config,

    supported_adapters={"~onebot.v11"},
)

from .libraries.FontUtil import font_init

deck_url = "https://gitee.com/fireinsect/image-save/raw/master/decks/"
font_url = "https://fastly.jsdelivr.net/gh/fireinsect/doc_save@0.1.0/fonts/"
fonts = ["msyh.ttc", "qmzl.ttf"]


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
                await asyncio.sleep(1)
    raise NetworkError(f"{url} 下载失败！请重新运行或者自行前往下载")


def save(wj_path: str, img: bytes):
    with open(wj_path, "wb") as f:  # 文件写入
        f.write(img)


async def download(base_url, folder_path, file_name):
    file_path = folder_path / file_name
    byte = await download_url(base_url + file_name)
    save(file_path, byte)
    logger.info(f"文件{file_name}下载成功")


# 卡运专用
async def download_img(files_path, file_name, deck):
    wj_path = files_path / file_name
    if not wj_path.exists():
        byte = await download_url(deck_url + f"{deck}/{file_name}")
        save(wj_path, byte)
        logger.info(f"图片{file_name}下载成功")


def deckDownloadInit():
    deck_json = Path(deck_path) / "deck_list.json"
    if not deck_json.exists():
        return
    with open(deck_json, 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
    for deck in js['list']:
        wjs_path = Path(deck_path) / deck
        if not wjs_path.exists():
            logger.info("文件夹decks/" + deck + " 不存在，已经创建")
            wjs_path.mkdir(parents=True, exist_ok=True)
        for wj in js['list'][deck]:
            asyncio.run(download_img(wjs_path, wj, deck))


def fontDownloadInit():
    if not Path(font_path).exists():
        Path(font_path).mkdir(parents=True, exist_ok=True)
    for font in fonts:
        if not (Path(font_path) / font).exists():
            logger.info(f"字体文件{font}缺失，正在下载")
            asyncio.run(download(font_url, Path(font_path), font))
    font_init()
    logger.info(f"字体初始化完成")


async def nickNameInit():
    nick_path = Path(json_path) / "nickname.json"
    try:
        # 尝试读取
        with open(nick_path, 'r', encoding='utf-8') as f:
            nick_json = json.loads(f.read())
            if isinstance(nick_json, dict):
                nick_json=nick_json['RECORDS']
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
    forbide_path = Path(json_path) / "forbidden.json"
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
    nick_path = Path(json_path) / "daily_card.json"
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


async def download_init():
    thread01 = Thread(target=deckDownloadInit)
    thread01.start()
    thread02 = Thread(target=fontDownloadInit)
    thread02.start()


async def init():
    logger.info("开始初始化")
    if not Path(pics_path).exists():
        logger.info("未发现图片文件夹，已经创建")
        (Path(pics_path) / "pics").mkdir(parents=True, exist_ok=True)
    await download_init()
    await nickNameInit()
    await forbideInit()
    await dailyInit()


driver = get_driver()
driver.on_startup(init)
