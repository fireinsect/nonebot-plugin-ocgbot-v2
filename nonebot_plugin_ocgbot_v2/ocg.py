import json

import nonebot
from nonebot.params import CommandArg

from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Event, Bot, GroupMessageEvent, PrivateMessageEvent, GROUP_ADMIN, \
    GROUP_OWNER
from nonebot import on_command

from nonebot_plugin_ocgbot_v2.libraries.Card import getCard, getRandomCard
from nonebot_plugin_ocgbot_v2.libraries.searchManage import SearchManager
from nonebot_plugin_ocgbot_v2.libraries.sendAction import *
from nonebot_plugin_ocgbot_v2.libraries.randomManage import RandomManager

pm = RandomManager()
sm = SearchManager()


# ==========工具变量、方法=============================


def verifySid(sid: str):
    try:
        sType, sId = sid.split('_')
        if sType in ['group', 'user']:
            if sId.isdigit():
                return True
        return False
    except:
        return False


# ===============功能==================================================


search_card = on_command("查卡")


@search_card.handle()
async def _(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
    if isinstance(event, GroupMessageEvent):
        sessionId = 'group_' + str(event.group_id)
    regex = "(.+) ([0-9]+)?"
    text = str(args).strip()
    if text == "":
        await search_card.finish("请输入需要查询的卡名")
    match = re.match(regex, text)
    try:
        search_group = match.groups()
        if search_group[1] is None:
            raise Exception()
    except:
        text = text + " 1"
        search_group = re.match(regex, text).groups()
    try:
        state['name'] = search_group[0]
        state['page'] = search_group[1]
        js = getCard(state['name'], state['page'])
    except Exception as e:
        await search_card.finish("咿呀？查询失败了呢")
    if int(search_group[1]) > int(js.pageNum):
        await search_card.finish("页码超出最大值" + "`" + str(js.pageNum) + "`")
    state['js'] = js
    if js.amount == 0:
        await sendNosearch(search_card)
    elif isinstance(event, PrivateMessageEvent):
        await send2(js, search_card)
    elif isinstance(event, GroupMessageEvent):
        typee = sm.CheckType(sessionId)
        state['send_type'] = typee
        if typee == 1:
            await send2(js, search_card)
        elif typee == 2:
            await send(js, bot, event, search_card)
        else:
            await send3(js, search_card)


@search_card.got("text", prompt="欧尼酱~输入任意语句或选择任意卡牌结束本次查卡~")
async def _(bot: Bot, event: Event, state: T_State):
    text = str(state['text'])
    js = state['js']
    if text.isdigit():
        if isinstance(event, PrivateMessageEvent):
            typee = 1
        elif isinstance(event, GroupMessageEvent):
            typee = int(state['send_type'])
        len = int(js.amount)
        chose = int(text)
        if 1 <= chose <= len:
            if typee == 1:
                await send2(js, search_card, chose)
            elif typee == 2:
                await send(js, bot, event, search_card, chose)
            else:
                await send3(js, search_card, chose)
    else:
        name = state['name']
        page = int(state['page'])
        flag = None
        if text == "下一页":
            if page == js.pageNum:
                await search_card.reject("欧尼酱~已经到最后一页了~")
            else:
                page = page + 1
                state['page'] = page
                flag = 1
        elif text == "上一页":
            if page == 1:
                await search_card.reject("欧尼酱~已经是第一页了~")
            else:
                page = page - 1
                state['page'] = page
                flag = 1
        else:
            await search_card.finish()
        if flag is not None:
            js = getCard(name, str(page))
            state['js'] = js
            if js.amount == 0:
                await sendNosearch(search_card)
            elif isinstance(event, PrivateMessageEvent):
                await send2(js, search_card)
            elif isinstance(event, GroupMessageEvent):
                typee = state['send_type']
                if typee == 1:
                    await send2(js, search_card)
                elif typee == 2:
                    await send(js, bot, event, search_card)
                else:
                    await send3(js, search_card)
            await search_card.reject("")


randomCard = on_command('随机一卡', aliases={'抽一张卡'})


@randomCard.handle()
async def _(bot: Bot, event: Event, state: T_State):
    groupSession = None
    sessionId = None
    if isinstance(event, PrivateMessageEvent):
        sessionId = 'user_' + str(event.user_id)
        userType = 'private'
    if isinstance(event, GroupMessageEvent):
        groupSession = 'group_' + str(event.group_id)
        sessionId = 'user_' + str(event.sender.user_id)
        userType = 'group'
    try:
        userType = 'SU' if (str(event.user_id) in nonebot.get_driver().config.superusers) else userType
        pm.CheckPermission(sessionId, groupSession, userType)
    except PermissionError as e:
        await randomCard.finish(str(e))
    try:
        js = getRandomCard()
        pm.UpdateLastSend(sessionId)
    except Exception as e:
        await randomCard.finish("咿呀？卡组被送进异次元了呢~")
    await send3(js, randomCard)


# ==========各类开关=============================

# ----- 抽卡cd时间更新 -----
random_cd = on_command("抽卡cd", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER, block=True, priority=10)


# 获取参数
@random_cd.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State, arg: Message = CommandArg()):
    message = str(arg).replace(" ", "")
    try:
        state['cdTime'] = int(str(message))
    except:
        await random_cd.finish(f'无效参数: {message}, 请输入 正整数 或 0 为参数')


# 群聊部分自动获取sid
@random_cd.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    sid = 'group_' + str(event.group_id)
    if not verifySid(sid):
        await random_cd.reject(f"无效目标对象: {sid}")
    await random_cd.finish(pm.UpdateCd(sid, state['cdTime']))


# 抽卡开关
ckpem = on_command("抽卡功能", permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@ckpem.handle()
async def cmdArg(bot: Bot, event: Event, state: T_State, message: Message = CommandArg()):
    if 'off' in str(message):
        state['add_mode'] = True
    elif 'on' in str(message):
        state['add_mode'] = False
    else:
        await ckpem.finish(f'无效参数: {message}, 请输入 on 或 off 为参数')


# 群聊部分自动获取sid
@ckpem.handle()
async def group(bot: Bot, event: GroupMessageEvent, state: T_State):
    state['sid'] = 'group_' + str(event.group_id)
    sid = str(state['sid'])
    if not verifySid(sid):
        await ckpem.reject(f"无效目标对象: {sid}")
    await ckpem.finish(pm.UpdateBanList(sid, state['add_mode']))


# 查卡方式
searchType = on_command("查卡方式")


@searchType.handle()
async def seartype(bot: Bot, event: GroupMessageEvent, state: T_State, args: Message = CommandArg()):
    message = str(args)
    state['sid'] = 'group_' + str(event.group_id)
    sid = str(state['sid'])
    if message.isdigit():
        if not verifySid(sid):
            await searchType.reject(f"无效目标对象: {sid}")
        await searchType.finish(sm.UpdateSearchType(sid, int(message)))
    else:
        await searchType.finish("请选择正确的方式")
