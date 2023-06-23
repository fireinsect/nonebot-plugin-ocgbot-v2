import json
import os.path
from nonebot import logger, get_driver
from nonebot_plugin_ocgbot_v2.libraries.forbideGet import forbiddenGet
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import json_path, static_path
from nonebot_plugin_ocgbot_v2.libraries.staticvar import nick_name_0, nick_name_1, forbidden, daily_card
from nonebot.plugin import PluginMetadata
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonbot-plugin-ocgbot-v2",
    description="提供游戏王相关服务",
    usage="提供包括查卡、随机抽卡、猜卡等功能",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/fireinsect/nonebot-plugin-ocgbot-v2/",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11", "~telegram"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)


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
    if not os.path.exists(static_path + "pics"):
        logger.info("未发现图片文件夹，已经创建")
        os.mkdir(static_path + "pics")
    await nickNameInit()
    await forbideInit()
    await dailyInit()


driver = get_driver()
driver.on_startup(init)