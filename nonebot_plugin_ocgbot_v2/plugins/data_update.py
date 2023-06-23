from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event
from nonebot.permission import SUPERUSER

from nonebot_plugin_ocgbot_v2.libraries.forbideGet import forbiddenGet
from nonebot_plugin_ocgbot_v2.libraries.staticvar import forbidden

forbidden_update = on_command('更新禁卡表', permission=SUPERUSER)


@forbidden_update.handle()
async def update(event: Event):
    forbidden.clear()
    await forbidden_update.send("欧尼酱，正在从官网下载禁卡表")
    forbiddenGet()
    await forbidden_update.finish("禁卡表更新成功~")
