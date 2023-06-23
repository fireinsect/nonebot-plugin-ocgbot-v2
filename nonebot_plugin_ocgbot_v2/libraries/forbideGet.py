import json

from requests_html import HTMLSession

from nonebot_plugin_ocgbot_v2.libraries.SqliteUtils import SqliteUtils
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import json_path, cdb_path
from nonebot_plugin_ocgbot_v2.libraries.staticvar import forbidden

url = "https://www.db.yugioh-card.com/yugiohdb/forbidden_limited.action?request_locale=ja#list_forbidden"
session = HTMLSession()
r = session.get(url)
bans_url = "#list_forbidden > div.list > div>div"
rests_url = "#list_limited > #forbidden_limited_list > div>div"
pres_url = "#list_semi_limited > #forbidden_limited_list > div>div"

# 禁止卡cid
bans = []
# 限制卡cid
rests = []
# 准限制卡cid
pres = []
sqlite = SqliteUtils()
conn, cursor = sqlite.connect(cdb_path + "cards.cdb")


def cidGet():
    global bans, rests, pres
    r = session.get(url)
    for k in list(r.html.find(bans_url)):
        bans.append(k.find("input")[0].attrs['value'].split("cid=")[1])
    for k in list(r.html.find(rests_url)):
        rests.append(k.find("input")[0].attrs['value'].split("cid=")[1])
    for k in list(r.html.find(pres_url)):
        pres.append(k.find("input")[0].attrs['value'].split("cid=")[1])


def forbideUpdate(card_id):
    cursor.execute(
        "select * from texts where id={0} ;".format(card_id)
    )
    re = cursor.fetchone()
    return re


def insert(card_id, name, status):
    json = {
        "card_id": card_id,
        "name": name,
        "status": status
    }
    forbidden.append(json)
    WriteForbidden(forbidden)


def WriteForbidden(js):
    # 写入数据
    with open(json_path + "forbidden.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(js, ensure_ascii=False, indent=4))


def forbiddenGet():
    cidGet()
    for i in bans:
        card_url = "https://ygocdb.com/?search=" + i
        re = session.get(card_url)
        card_id = list(re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(4) > span:nth-child(1)"))
        if len(card_id) == 0:
            card_id = list(re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(3) > span:nth-child(1)"))[0].text
        else:
            card_id = card_id[0].text
        name = forbideUpdate(card_id)['name']
        insert(card_id, name, "禁")
    for i in rests:
        card_url = "https://ygocdb.com/?search=" + i
        re = session.get(card_url)
        card_id = list(re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(4) > span:nth-child(1)"))
        if len(card_id) == 0:
            card_id = re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(3) > span:nth-child(1)")[0].text
        else:
            card_id = card_id[0].text
        name = forbideUpdate(card_id)['name']
        insert(card_id, name, "限")
    for i in pres:
        card_url = "https://ygocdb.com/?search=" + i
        re = session.get(card_url)
        card_id = list(re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(4) > span:nth-child(1)"))
        if len(card_id) == 0:
            card_id = list(re.html.find("div.col-md-6.col-xs-8.names > h3:nth-child(3) > span:nth-child(1)"))[0].text
        else:
            card_id = card_id[0].text
        name = forbideUpdate(card_id)['name']
        insert(card_id, name, "准限")
