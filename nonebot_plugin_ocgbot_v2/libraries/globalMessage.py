import os.path
import pathlib

import nonebot
from nonebot import Config, logger

random_sendwitchoutcd=[
    "臭欧尼酱！慢点啦！",
    "前面的区域之后再来探索吧~",
    "臭欧尼酱又在抽卡哦~休息一下好不好~",
    "臭欧尼酱小蓝不让你抽卡了(叉腰)~",
    "抽多了对身体不好❤️~臭哥哥受不了的~",
    "杂鱼又在抽卡呀，天天只会抽卡，真是飞舞❤️～",
    "笨蛋大叔，着什么急❤️～笨蛋❤️笨蛋",
    "臭大叔，不给你抽了！生气了吗？嘻嘻❤️～"
]
guess_sendwitchoutcd=[
    "打咩❤️！",
    "前面的区域之后再来探索吧~",
    "臭欧尼酱！慢点啦！",
    "臭欧尼酱小蓝不让你猜卡了(叉腰)~",
    "臭欧尼酱又在猜卡哦~休息一下好不好~",
    "杂鱼又在猜卡呀，天天只会猜卡，真是飞舞❤️～",
    "笨蛋大叔，着什么急❤️～笨蛋❤️笨蛋",
    "臭大叔，不给你猜了！生气吗？生气吗❤️？"
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
guess_tips = [
    "\r\n呃啊~臭哥哥❤~这都不会？我偷偷告诉你这张卡{0}。",
    "\r\n杂鱼❤~杂鱼❤~，这张卡{0}~",
    "\r\n杂鱼哥哥真好捉弄❤~。这张卡{0}~",
    "\r\n好❤恶❤心~，连这张卡{0}都不知道❤~",
    "\r\n杂❤~鱼❤~这张卡是{0}~"
]
guess_lose = [
    "\r\n这都猜不到，臭哥哥就是弱哎❤，答案是{0}",
    "\r\n略略略❤~猜不到吧，答案是{0}",
    "\r\n笨蛋哥哥果然是杂❤鱼，连这个是{0}都猜不到？",
    "\r\n弱哎❤~这就不行了，答案是{0}哎~"
]
guess_skip = [
    "\r\n略略略❤~臭哥哥这就不行了？答案是{0}",
    "\r\n就这❤~就这❤~答案是{0}",
    "\r\n杂鱼哥哥这就结束了❤？答案是{0}",
    "\r\n弱哎❤~哥哥好弱❤~答案是{0}"
]
guess_win = [
    "\r\n哎，竟然答对了吗？真无聊❤~答案就是{0}啦",
    "\r\n杂鱼哥哥竟然答对了❤~答案是{0}",
    "\r\n好吧，好吧，算你对了啦❤~答案就是{0}",
    "\r\n恶心！变态！竟然答对了❤~答案是{0}"
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
deck_path = static_path_abso + "decks/"
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
        if os.path.exists(static_path_config + "decks/"):
            deck_path = static_path_config + "decks/"
            logger.info("环境路径存在deck文件夹，已使用")
except:
    logger.info("不存在环境路径，使用本地路径....")
