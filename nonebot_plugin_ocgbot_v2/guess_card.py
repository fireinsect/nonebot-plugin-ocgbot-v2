import json
import math
import random
import sys
from pathlib import Path

import nonebot
import requests
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from nonebot_plugin_ocgbot_v2.libraries.Card import getRandomCard, getCard
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import *

sys.path.append(str(Path(__file__).resolve().parents[1]))  # 将父级目录加入执行目录列表
from nonebot_plugin_ocgbot_v2.libraries.image import *
from nonebot_plugin_ocgbot_v2.libraries.tool import getRandom
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, MessageSegment, MessageEvent, \
    PrivateMessageEvent, \
    Message, GROUP_ADMIN, GROUP_OWNER
from nonebot.typing import T_State
from typing import Dict, Optional
from nonebot_plugin_ocgbot_v2.libraries.guessManage import guessCardManager

# test = '{"status":200,"msg":"获取成功","data":{"cards":[{"id":9107,"cardId":75109441,"name":"半蛇人 萨库兹","effect":"这张卡1个回合可以有1次变回里侧守备表示。这张卡反转时，对方场上的盖伏的全部魔法·陷阱卡翻开，确认后变回原来的盖伏形式。","zz":"爬虫类族","mainType":"怪兽","type":"怪兽 效果","level":"3 星","attribute":"地","atk":"800","def":"1400","jpName":"半蛇人サクズィー","enName":"Cobraman Sakuzy","forbidden":"-"}],"pageNum":1,"amount":1,"nowNum":1},"isSuccess":true}'
# test2=json.loads(test)
# li=json.dumps( list(test2['data']['cards'])[0])
# print(li)
# card = json.loads(li,object_hook=Card)
# print(card.cardId)
# print(card.deff)

cardUrl = pics_path
guessCard = on_command('游戏王猜卡', aliases={'猜一张卡'})
aiguessCard = on_command('ai猜卡')
gm = guessCardManager()
RESIZE = guess_diff[0].get("resize")
CUTSIZE = guess_diff[0].get("cutsize")
TIME = guess_diff[0].get("time")


# ai猜卡常量
# 本地图片应为 cardId+.jpg形式命名 存放在static/aicard 文件夹下
# cardImgPath = static_path_abso+"aicard/"
# img_list = os.listdir(cardImgPath)


# 根据会话类型生成sessionId
def sessionId(event: MessageEvent):
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
    if isinstance(event, GroupMessageEvent):
        sessionId = 'group_' + str(event.group_id)
    return sessionId


def verifySid(sid: str):
    try:
        sType, sId = sid.split('_')
        if sType in ['group', 'user']:
            if sId.isdigit():
                return True
        return False
    except:
        return False

# ai猜卡（自定义猜卡功能，发送本地图片进行猜卡）
# @aiGuessCard.handle()
# async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
#     sessionId = None
#     groupSession = None
#     # 根据会话类型生成sessionId
#     if isinstance(event, PrivateMessageEvent):
#         sessionId = 'user_' + str(event.user_id)
#         userType = 'private'
#     if isinstance(event, GroupMessageEvent):
#         groupSession = 'group_' + str(event.group_id)
#         sessionId = 'user_' + str(event.sender.user_id)
#         userType = 'group'
#         # 权限检查
#     try:
#         userType = 'SU' if (str(event.user_id) in nonebot.get_driver().config.superusers) else userType
#         gm.CheckPermission(sessionId, groupSession, userType)
#     except PermissionError as e:
#         await aiGuessCard.finish(str(e))
#     try:
#         rand = random.randint(0, len(img_list))
#         id = str(img_list[rand]).split('.')[0]
#         js = getCard(id)
#         card = js.cards[0]
#         state['card'] = card
#         # 自定义卡图
#         pics_url = cardImgPath + str(card.cardId) + ".jpg"
#         image = Image.open(pics_url)
#         print(card.name)
#         state['time'] = TIME
#         # 源卡图
#         ori_pics_url = cardUrl + str(card.cardId) + ".jpg"
#         ori_image = Image.open(ori_pics_url)
#         state['image'] = ori_image
#         gm.UpdateLastSend(sessionId)
#         await aiGuessCard.send([
#             MessageSegment.at(user_id=event.sender.user_id),
#             MessageSegment.text(text=get_named()"，你有三次机会哟~(输入跳过结束游戏)"),
#             MessageSegment.image(f"base64://{str(image_to_base64(image), encoding='utf-8')}")
#         ])
#     except Exception as e:
#         print(e)
#         await aiGuessCard.finish("咿呀？启动失败了呢")
#
#
# @aiguessCard.got("name")
# async def test_(bot: Bot, event: GroupMessageEvent, state: T_State):
#     name = str(state['name'])
#     card = state['card']
#     if name == "不知道" or name == "跳过":
#         await aiGuessCard.finish([
#             MessageSegment.at(user_id=event.sender.user_id),
#              MessageSegment.text(text=guess_skip().format(card.name)),
#             MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
#         ])
#
#     js = getCard(name)
#     # card.name != js.cards[0].name
#     if js.cards is None or isGuessWin(js, card.name):
#         if state['time'] == 1:
#             await aiGuessCard.finish([
#                 MessageSegment.at(user_id=event.sender.user_id),
#                 MessageSegment.text(text=guess_lose().format(card.name)),
#                 MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
#             ])
#         else:
#             if state['time'] == 3:
#                 hint = MessageSegment.text(
#                     text=guess_tips().format("是" + card.mainType + "卡"))
#             elif state['time'] == 2:
#                 if card.mainType == '怪兽':
#                     ran = random.randint(0, 2)
#                     if ran == 0:
#                         hint = MessageSegment.text(
#                             text=guess_tips().format("种族是" + card.zz))
#
#                     elif ran == 1:
#                         hint = MessageSegment.text(
#                             text=guess_tips().format("属性是" + card.attribute))
#
#                     else:
#                         hint = MessageSegment.text(
#                             text=guess_tips().format("完整类型是" + card.type))
#                 else:
#                     hint = MessageSegment.text(
#                         text=guess_tips().format("完整类型是" + card.type))
#             state['time'] = state['time'] - 1
#             await aiGuessCard.reject([
#                 MessageSegment.at(user_id=event.sender.user_id),
#                 hint,
#                 MessageSegment.text(text="\r\n还有{0}次机会！".format(state['time']))
#             ])
#     else:
#         await aiguessCard.finish([
#             MessageSegment.at(user_id=event.sender.user_id),
#             MessageSegment.text(text=guess_win().format(card.name)),
#             MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
#         ])


@guessCard.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    # 根据会话类型生成sessionId
    sessionId = None
    groupSession = None
    # 根据会话类型生成sessionId
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        groupSession = 'group_' + str(event.group_id)
        sessionId = 'user_' + str(event.sender.user_id)
        userType = 'group'
        # 权限检查
    try:
        userType = 'SU' if (str(event.user_id) in nonebot.get_driver().config.superusers) else userType
        gm.CheckPermission(sessionId, groupSession, userType)
    except PermissionError as e:
        await guessCard.finish(str(e))
    try:
        js = getRandomCard()
        card = js.cards[0]
        state['card'] = card
        pics_url = cardUrl + str(card.cardId) + ".jpg"
        try:
            image = Image.open(pics_url)
        except Exception as e:
            await guessCard.send("没找到对应图片~")
        re_image = image
        if "灵摆" in card.type:
            image = image.crop((30, 110, 370, 357))
        else:
            image = image.crop((52, 110, 348, 407))
        image = getGuessImg(image)
        state['time'] = TIME
        state['image'] = re_image
        gm.UpdateLastSend(sessionId)
        await guessCard.send([
            MessageSegment.at(user_id=event.sender.user_id),
            MessageSegment.text(text=get_named()+"臭欧尼酱，你有三次机会哟~(输入跳过结束游戏)"),
            MessageSegment.image(f"base64://{str(image_to_base64(image), encoding='utf-8')}")
        ])
    except Exception as e:
        await guessCard.finish("咿呀？启动失败了呢")


@guessCard.got("name")
async def test_(bot: Bot, event: GroupMessageEvent, state: T_State):
    name = str(state['name'])
    card = state['card']
    if name == "不知道" or name == "跳过":
        await guessCard.finish([
            MessageSegment.at(user_id=event.sender.user_id),
            MessageSegment.text(text=guess_skip().format(card.name)),
            MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
        ])
    js = getCard(name)
    if js.cards is None or isGuessWin(js, card.name, name):
        if state['time'] == 1:
            await guessCard.finish([
                MessageSegment.at(user_id=event.sender.user_id),
                MessageSegment.text(text=guess_lose().format(card.name)),
                MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
            ])
        else:
            if state['time'] == 3:
                hint = MessageSegment.text(
                    text=guess_tips().format("是" + card.mainType + "卡"))
            elif state['time'] == 2:
                if card.mainType == '怪兽':
                    ran = random.randint(0, 2)
                    if ran == 0:
                        hint = MessageSegment.text(
                            text=guess_tips().format("种族是" + card.zz))
                    elif ran == 1:
                        hint = MessageSegment.text(
                            text=guess_tips().format("属性是" + card.attribute))
                    else:
                        hint = MessageSegment.text(
                            text=guess_tips().format("完整类型是" + card.type))
                else:
                    hint = MessageSegment.text(
                        text=guess_tips().format("完整类型是" + card.type))
            state['time'] = state['time'] - 1
            await guessCard.reject([
                MessageSegment.at(user_id=event.sender.user_id),
                hint,
                MessageSegment.text(text="\r\n还有{0}次机会！".format(state['time']))
            ])
    else:
        await guessCard.finish([
            MessageSegment.at(user_id=event.sender.user_id),
            MessageSegment.text(text=guess_win().format(card.name)),
            MessageSegment.image(f"base64://{str(image_to_base64(state['image']), encoding='utf-8')}")
        ])


# 猜卡结果判断
def isGuessWin(js, cardName, name) -> bool:
    if name is cardName:
        return False
    if js.amount <= 5:
        for card in js.cards:
            if card.name == cardName:
                return False
    else:
        if js.cards[0].name == cardName:
            return False
    return True


# -----获取猜卡卡图 -----
def getGuessImg(image: Image, restrict=2) -> Image:
    height, weight = image.size
    # 模糊处理
    if getRandom(restrict) == 1:
        image.thumbnail((height / RESIZE, weight / RESIZE), Image.ANTIALIAS)
        height, weight = image.size
        image = image.resize((height * RESIZE, weight * RESIZE))
    # 切割处理
    else:
        sqrt = math.sqrt(CUTSIZE)
        beSqrt = CUTSIZE / sqrt
        cut = (sqrt, beSqrt) if getRandom(2) == 1 else (beSqrt, sqrt)
        cutHeight, cutWeight = int(image.size[0] / cut[0]), int(image.size[1] / cut[1])
        cutX, cutY = random.randint(cutHeight, height - cutHeight), random.randint(cutWeight, weight - cutWeight)
        image = image.crop((cutX, cutY, cutX + cutHeight, cutY + cutWeight))
    return image


# ----- 抽卡cd时间更新 -----
guess_cd = on_command("猜卡cd", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER, block=True, priority=10)


# 获取参数
@guess_cd.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    message = str(args).replace(" ", "")
    try:
        state['cdTime'] = int(str(message))
    except:
        await guess_cd.finish(f'无效参数: {message}, 请输入 正整数 或 0 为参数')


# 群聊部分自动获取sid
@guess_cd.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    sid = 'group_' + str(event.group_id)
    if not verifySid(sid):
        await guess_cd.reject(f"无效目标对象: {sid}")
    await guess_cd.finish(gm.UpdateCd(sid, state['cdTime']))


# ----- 黑名单添加与解除 -----
ban_guess = on_command("猜卡功能", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER, block=True, priority=10)


# 分析是新增还是删除
@ban_guess.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State, message: Message = CommandArg()):
    if 'off' in str(message):
        state['add_mode'] = True
    elif 'on' in str(message):
        state['add_mode'] = False
    else:
        await ban_guess.finish(f'无效参数: {message}, 请输入 on 或 off 为参数')


# 群聊部分自动获取sid
@ban_guess.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    sid = 'group_' + str(event.group_id)
    if not verifySid(sid):
        await ban_guess.reject(f"无效目标对象: {sid}")
    await ban_guess.finish(gm.UpdateBanList(sid, state['add_mode']))


class Card(Dict):
    id: Optional[int] = None
    cardId: Optional[int] = None
    name: Optional[str] = None
    effect: Optional[str] = None
    zz: Optional[str] = None
    mainType: Optional[str] = None
    type: Optional[str] = None
    level: Optional[str] = None
    attribute: Optional[str] = None
    atk: Optional[str] = None
    deff: Optional[str] = None
    forbidden: Optional[str] = None

    def __getattribute__(self, item):
        if item in {'id', 'cardId', 'name', 'effect', 'zz', 'mainType', 'type', 'level', 'attribute', 'atk', 'deff',
                    'forbidden'}:
            if item == 'deff':
                return self['def']
            return self[item]
        return super().__getattribute__(item)
