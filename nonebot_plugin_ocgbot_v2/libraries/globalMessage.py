import os.path
import pathlib

import nonebot
from nonebot import Config, logger

random_sendwitchoutcd = [
    "欧尼酱！慢点慢点！",
    "前面的区域之后再来探索吧~",
    "欧尼酱又在抽卡哦~休息一下好不好~",
    "小蓝拒绝了欧尼酱的抽卡(叉腰)~",
    "抽多了对身体不好~",
]
guess_sendwitchoutcd = [
    "打咩！",
    "前面的区域之后再来探索吧~",
    "欧尼酱！慢点慢点！",
    "小蓝拒绝了欧尼酱的猜卡(叉腰)~",
    "欧尼酱又在猜卡哦~休息一下好不好~",
]

noSearchText = [
    "没找到捏~ 欧尼酱~",
    "咦？这张卡不存在呢",
    "哔哔~卡片不存在"
]

lanName = [
    "今天有没有好好打牌呢？",
    "适度打牌，注意休息",
    "废物小蓝，嗷呜嗷呜",
    "可可爱爱，没有脑袋",
    "小蓝(洗衣服ing)",
    "你看你脏的，让我洗！",
    "呜，不会打牌唔",
    "摸鱼的G",
    "小蓝(非卖品)",
    "今天堆点什么捏?",
    "嘟嘟嘟，小蓝警长"
]
# 猜卡难度
guess_diff = [
    {
        'resize': 7,
        'cutsize': 6,
        'time': 3
    }
]
static_path_abso = str(pathlib.Path(__file__).parent.parent).replace("\\", "/") + "/static/"
json_path = static_path_abso + "json/"
font_path = static_path_abso + "fonts/"
cdb_path = static_path_abso + "cdb/"
image_path = static_path_abso + "images/"
pics_path = static_path_abso + "pics/"
deck_path = static_path_abso + "deck/"
logger.info("静态文件路径检查中......")
try:
    static_path_config = str(Config.parse_obj(nonebot.get_driver().config).static_path)
    logger.info(static_path_config)
    if not (static_path_config.endswith("/") or static_path_config.endswith("\\")):
        static_path_config = static_path_config + "/"
    if not os.path.exists(static_path_config):
        logger.info("环境路径不存在.....")
    else:
        if os.path.exists(static_path_config + "json/"):
            json_path = static_path_config + "json/"
            logger.info("环境路径存在json文件夹，已使用")
        if os.path.exists(static_path_config + "fonts/"):
            font_path = static_path_config + "fonts/"
            logger.info("环境路径存在fonts文件夹，已使用")
        if os.path.exists(static_path_config + "cdb/"):
            cbd_path = static_path_config + "cdb/"
            logger.info("环境路径存在cdb文件夹，已使用")
        if os.path.exists(static_path_config + "images/"):
            image_path = static_path_config + "images/"
            logger.info("环境路径存在images文件夹，已使用")
        if os.path.exists(static_path_config + "pics/"):
            pics_path = static_path_config + "pics/"
            logger.info(pics_path)
            logger.info("环境路径存在pics文件夹，已使用")
        if os.path.exists(static_path_config + "deck/"):
            deck_path = static_path_config + "deck/"
            logger.info("环境路径存在deck文件夹，已使用")
except:
    logger.info("不存在环境路径，使用本地路径....")
