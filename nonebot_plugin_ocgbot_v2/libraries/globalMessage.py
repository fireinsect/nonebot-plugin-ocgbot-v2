from pathlib import Path
from random import choice
from nonebot import logger

from ..config import config

# 猜卡难度
guess_diff = [
    {
        'resize': 7,  # 模糊缩放比例
        'cutsize': 6,  # 裁剪比例
        'time': 3,  # 猜卡次数
        'timeout': 30  # 答案公布时间
    }
]
# 查询失败语录
noSearchText = [
    "没找到捏~ 欧尼酱~",
    "咦？这张卡不存在呢",
    "哔哔~卡片不存在"
]
# 合并消息显示昵称
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
# 文本选择 当前0：雌小鬼语录 1：正常语录
mess_type_choose = 1

# 消息发送文本信息 ##表示称呼替代
message_type = [
    {
        'guess': {
            'sendwitchoutcd': [
                "打咩❤️！",
                "前面的区域之后再来探索吧~",
                "##！慢点啦！",
                "##,小蓝不让你猜卡了(叉腰)~",
                "##又在猜卡哦~休息一下好不好~",
                "##又在猜卡呀，天天只会猜卡，真是飞舞❤️～",
                "笨蛋##，着什么急❤️～笨蛋❤️笨蛋",
                "##，不给你猜了！生气吗？生气吗❤️？"
            ],
            'tips': [
                "呃啊~##❤~这都不会？我偷偷告诉你这张卡{0}。",
                "##❤~##❤~，这张卡{0}~",
                "##真好捉弄❤~。这张卡{0}~",
                "好❤恶❤心~，连这张卡{0}都不知道❤~",
                "杂❤~鱼❤~这张卡是{0}~",
                "哎~这么简单的题都不会，这张卡是{0}❤~",
                "行不行啊~##❤~连这张卡是{0}都不知道~",
                "这张卡小蓝三岁就会了，##连它是{0}都不知道❤~",
                "呐❤~呐❤~呐❤~##不会是笨蛋吧，这张卡是{0}呀~",
            ],
            'lose': [
                "这都猜不到，##就是弱哎❤，答案是{0}",
                "略略略❤~猜不到吧，答案是{0}",
                "##果然是杂❤鱼，连这个是{0}都猜不到？",
                "弱哎❤~这就不行了，答案是{0}哎~",
                "行不行啊❤~##，连{0}都猜不到~",
                "不是吧❤~这都猜不到❤~，答案是{0}",
                "##❤~##❤~答案是{0}~",
                "就这啊~##❤~答案是{0}哦~",
                "##❤~连{0}都答不上来~真是飞舞❤~",
                "不会吧❤不会吧❤不会有人连{0}都猜不到吧❤",
                "##！告诉你答案吧！是{0}！"
            ],
            'skip': [
                "略略略❤##这就不行了？答案是{0}",
                "就这❤~就这❤~答案是{0}",
                "##这就结束了❤？答案是{0}",
                "弱哎❤~##好弱❤~答案是{0}",
                "就这啊~##❤~答案是{0}哦~",
                "不会吧❤不会吧❤不会有人连{0}都猜不到吧❤",
                "##也太❤弱❤了❤吧，答案是{0}耶~",
                "##❤~连{0}都答不上来~真是飞舞❤~",
                "行不行啊❤~##，连{0}都猜不到~",
            ],
            'timeout': [
                "时间到啦！##连这都不会吗？答案是{0}",
            ],
            'win': [
                "哎，竟然答对了吗？真无聊❤~答案就是{0}啦",
                "##竟然答对了❤~答案是{0}",
                "好吧，好吧，算你对了啦❤~答案就是{0}",
                "恶心！变态！竟然答对了❤~答案是{0}",
                "答错...好吧,##竟然答对了{0}(生气)",
                "呐❤呐❤呐❤，##竟然答对了{0},##不会作弊了吧❤~"
            ],
        },
        'random': {
            'sendwitchoutcd': [
                "##！慢点啦！",
                "前面的区域之后再来探索吧~",
                "##又在抽卡哦~休息一下好不好~",
                "##小蓝不让你抽卡了(叉腰)~",
                "抽多了对身体不好❤~##受不了的~",
                "##又在抽卡呀，天天只会抽卡，真是飞舞❤～",
                "##，着什么急❤～笨蛋❤笨蛋",
                "##，不给你抽了！生气了吗？嘻嘻❤～"
            ]
        }
    },

    {
        'guess': {
            'sendwitchoutcd': [
                "打咩️！",
                "前面的区域之后再来探索吧~",
                "##！慢点啦！",
                "##,小蓝不让你猜卡了(叉腰)~",
                "##又在猜卡哦~休息一下好不好~",
                "##又在猜卡呀,不要猜卡了好不好~",
                "##，稍等一下，小蓝在准备卡组~",
                "##，不要猜卡啦，让小蓝休息一下吧QAQ",
                "洗衣服中（勿扰）"
            ],
            'tips': [
                "##答不出来吗，小蓝提醒你一下这张卡{0}。",
                "##！##！这张卡{0}啦！",
                "唔...这张卡{0}小蓝偷偷告诉##，不要告诉别人哦~",
                "嘟嘟嘟~这张卡{0}哦~",
                "（翻阅卡表）这张卡是{0}哦~（叉腰）",
                "呀！好像题目有点难，小蓝提醒一下##吧，这张卡是{0}~",
                "哎~##猜不到吗？这张卡是{0}",
                "这张卡{0}！快猜快猜，猜完小蓝要去洗衣服了",
            ],
            'lose': [
                "啊！##没猜出来吗！答案是{0}啦",
                "##！##！错了啦！答案是{0}啦",
                "（翻阅卡表）答案好像是{0}哎？##没猜出来，好可惜哦~",
                "嘟嘟嘟，答案新鲜出炉！是{0}哒~",
                "答案是{0}哦~，##再接再厉吧~",
            ],
            'skip': [
                "啊！##猜不到吗！答案是{0}啦",
                "##！##！！答案是{0}啦",
                "（翻阅卡表）答案好像是{0}哎？##没猜出来，好可惜哦~",
                "嘟嘟嘟，答案新鲜出炉！是{0}哒~",
                "答案是{0}哦~，##再接再厉吧~",
                "QWQ既然##不会，那么小蓝告诉你答案吧，是{0}哦~"
            ],
            'timeout': [
                "时间到啦！答案是{0}哦~",
            ],
            'win': [
                "##好厉害！答案就是{0}啦",
                "##答对了！（崇拜眼）答案是{0}",
                "哇！欧尼酱答对啦！好厉害鸭！答案就是{0}",
                "呼呼呼！##答对啦，答案是{0}，下次小蓝要出更难的题（比拳头）",
                "好耶,##答对了{0}！小蓝可以去洗衣服啦",
                "嘿嘿嘿，##好厉害，小蓝都不会呢，答案就是{0}哦"
            ],
        },
        'random': {
            'sendwitchoutcd': [
                "##！慢点啦！",
                "前面的区域之后再来探索吧~",
                "##又在抽卡哦~休息一下好不好~",
                "##小蓝不让你抽卡了(叉腰)~",
                "抽多了对身体不好,##受不了的啦",
                "##，不要着急啦",
                "##，不给你抽了啦！"
            ]
        }
    },
]


def random_sendwitchoutcd() -> str:
    arr = message_type[mess_type_choose]['random']['sendwitchoutcd']
    return choice(arr).replace("##", get_named())


def guess_sendwitchoutcd() -> str:
    arr = message_type[mess_type_choose]['guess']['sendwitchoutcd']
    return choice(arr).replace("##", get_named())


# guess_tips = [
#     "这张卡{0}。",
# ]

# ##字当作称呼的替换符
def guess_tips() -> str:
    arr = message_type[mess_type_choose]['guess']['tips']
    return "\r\n" + choice(arr).replace("##", get_named())


def guess_lose() -> str:
    arr = message_type[mess_type_choose]['guess']['lose']
    return "\r\n" + choice(arr).replace("##", get_named())


def guess_skip() -> str:
    arr = message_type[mess_type_choose]['guess']['skip']
    return "\r\n" + choice(arr).replace("##", get_named())


def guess_timeout() -> str:
    arr = message_type[mess_type_choose]['guess']['timeout']
    return choice(arr).replace("##", get_named())


def guess_win() -> str:
    arr = message_type[mess_type_choose]['guess']['win']
    return "\r\n" + choice(arr).replace("##", get_named())


# 称呼信息
def get_named() -> str:
    arr = [
        [
            "臭哥哥",
            "哥哥",
            "臭欧尼酱",
            "欧尼酱",
            "杂鱼",
            "臭杂鱼",
            "杂鱼哥哥",
            "大叔",
            "臭大叔"
        ],
        [
            "欧尼酱",
            "哥哥",
            "哥哥大人",
        ]

    ]
    return choice(arr[mess_type_choose])


static_path_abso = Path(__file__).parent.parent / "static"
paths = {}
json_path = str(static_path_abso / "json")
font_path = str(static_path_abso / "fonts")
cdb_path = str(static_path_abso / "cdb")
image_path = str(static_path_abso / "images")
pics_path = str(static_path_abso / "pics")
deck_path = str(static_path_abso / "decks")
logger.info("静态文件路径检查中......")
try:
    static_path_config = Path(config.static_path)
    logger.info(static_path_config)
    # if not (static_path_config.endswith("/") or static_path_config.endswith("\\")):
    #     static_path_config = static_path_config + "/"
    if not static_path_config.exists():
        logger.info("环境路径不存在.....")
    else:
        if (static_path_config / "json").exists():
            json_path = str(static_path_config / "json")
            logger.info("环境路径存在json文件夹，已使用")
        if (static_path_config / "fonts").exists():
            font_path = str(static_path_config / "fonts")
            logger.info("环境路径存在fonts文件夹，已使用")
        if (static_path_config / "cdb").exists():
            cdb_path = str(static_path_config / "cdb")
            logger.info("环境路径存在cdb文件夹，已使用")
        if (static_path_config / "images").exists():
            image_path = str(static_path_config / "images")
            logger.info("环境路径存在images文件夹，已使用")
        if (static_path_config / "pics").exists():
            pics_path = str(static_path_config / "pics")
            logger.info("环境路径存在pics文件夹，已使用")
        if (static_path_config / "decks").exists():
            deck_path = str(static_path_config / "decks")
            logger.info("环境路径存在deck文件夹，已使用")
except:
    logger.info("不存在环境路径，使用本地路径....")
