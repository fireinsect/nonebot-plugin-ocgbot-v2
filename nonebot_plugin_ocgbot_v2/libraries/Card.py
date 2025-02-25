import copy
import json
import math
from pathlib import Path
from typing import Optional, Dict
import httpx
from nonebot_plugin_ocgbot_v2.libraries.SqliteUtils import SqliteUtils
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import cdb_path
from nonebot_plugin_ocgbot_v2.libraries.staticvar import forbidden, nick_name_0, nick_name_1

sqlite = SqliteUtils()

pre_flag = 0
extra_flag = 0
conn, cursor = sqlite.connect(Path(cdb_path) / "cards.cdb")

if (Path(cdb_path) / "pre-release.cdb").exists():
    conn_pre, cursor_pre = sqlite.connect(Path(cdb_path) / "pre-release.cdb")
    pre_flag = 1
elif(Path(cdb_path) / "test-release.cdb").exists():
    conn_pre, cursor_pre = sqlite.connect(Path(cdb_path) / "test-release.cdb")
    pre_flag = 1

if (Path(cdb_path) / "extra_card.cdb").exists():
    conn_extra, cursor_extra = sqlite.connect(Path(cdb_path) / "extra_card.cdb")
    extra_flag = 1

typeList = ['怪兽', '魔法', '陷阱']
bg_url = "https://ygocdb.com/api/v0/?search="

hasType = [
    ["怪兽", "魔法", "陷阱", "N/A"],
    ["通常", "效果", "融合", "仪式"],
    ["N/A", "灵魂", "同盟", "二重"],
    ["调整", "同调", "衍生物", "N/A"],
    ["速攻", "永续", "装备", "场地"],
    ["反击", "反转", "卡通", "超量"],
    ["灵摆", "特殊召唤", "连接", "N/A"]
]
hasZz = [
    ["战士族", "魔法师族", "天使族", "恶魔族"],
    ["不死族", "机械族", "水族", "炎族"],
    ["岩石族", "鸟兽族", "植物族", "昆虫族"],
    ["雷族", "龙族", "兽族", "兽战士族"],
    ["恐龙族", "鱼族", "海龙族", "爬虫类族"],
    ["念动力族", "幻神兽族", "创造神族", "幻龙族"],
    ["电子界族", "幻想魔族", "N/A", "N/A"],

]
hasAttribute = [
    ["地", "水", "炎", "风"],
    ["光", "暗", "神", ""]
]
pagesize = 5


class Card_Extra(Dict):
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
    forbidden: Optional[str] = "-"

    def __getattribute__(self, item):
        if item in {'cardId', 'name', 'effect', 'zz', 'mainType', 'type', 'level', 'attribute', 'atk', 'deff'}:
            if item == 'cardId':
                return self['id']
            if item == 'deff':
                return self['def']
            return self[item]
        return super().__getattribute__(item)


class Card(Dict):
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
    forbidden: Optional[str] = "-"

    def __getattribute__(self, item):
        if item in {'cardId', 'name', 'effect', 'zz', 'mainType', 'type', 'level', 'attribute', 'atk', 'deff'}:
            types = getType(str(hex(self['type'])))
            if item == 'cardId':
                return self['id']
            if item == 'type':
                return ' '.join(types)
            if item == 'mainType':
                return types[0]
            if item == "zz":
                return getZz(str(hex(self['race'])))
            if item == "atk":
                if types[0] == "怪兽":
                    return str(self[item]) if str(self[item]) != "-2" else "?"
                else:
                    return None
            if item == "deff":
                if types[0] == "怪兽" and "连接" not in types:
                    return str(self['def']) if str(self['def']) != "-2" else "?"
                else:
                    return None
            if item == "attribute":
                return getAttribute(str(hex(self['attribute'])))

            if item == "level":
                level = self['level']&0xffff
                if "连接" in types:
                    return "Link " + str(level)
                elif "超量" in types:
                    return str(level) + " 阶"
                else:
                    return str(level) + " 星"
            if item == "effect":
                return self['desc'].replace("\r", "")
            return self[item]

        return super().__getattribute__(item)


class CardResult(Dict):
    cards: Optional[list] = None
    pageNum: Optional[int] = None
    amount: Optional[int] = None
    nowNum: Optional[int] = None


def getType(datas) -> list:
    datas = datas.replace("0x", "")
    types = []
    n = len(datas)
    for i in range(1, 8):
        if n >= i:
            c = datas[n - i]
            if c in ['a', 'b', 'c', 'd', 'e', 'f']:
                c = bin(ord(c) - 87)
            else:
                c = bin(int(c))
            line = c.replace("0b", "")
            for j in range(len(line)):
                if line[j] == '1':
                    types.append(hasType[i - 1][len(line) - j - 1])
        else:
            break
    return types


def getZz(datas):
    datas = datas.replace("0x", "")
    # bin多两位进制指示符
    return hasZz[len(datas) - 1][len(bin(int(datas[0]))) - 3]


def getAttribute(datas):
    datas = datas.replace("0x", "")
    # bin多两位进制指示符
    return hasAttribute[len(datas) - 1][len(bin(int(datas[0]))) - 3]


def getCard(name: str, page="1") -> CardResult:
    if page is None or page.replace(" ", "") == "":
        page = "1"
    pageint = int(page)
    if name.isdigit():
        cards = searchById(int(name))
        if len(cards) == 0:
            cards = searchByName(name)  # 这里写name获取方法
    else:
        cards = searchByName(name)  # 这里写name获取方法
    return getCardResult(cards, pageint)  # 这里写分页算法


def getRandomCard() -> CardResult:
    sql = "SELECT * FROM texts LEFT JOIN datas on texts.id=datas.id where name= (SELECT name FROM texts ORDER BY RANDOM() limit 1) GROUP BY texts.name;"
    cursor.execute(sql)
    card = [Card(cursor.fetchall()[0])]
    return getCardResult(card, 1)


def getCardResult(cards, page):
    cardResult = CardResult()
    cards = forbiddenChange(cards)
    cardResult.amount = len(cards)
    cardResult.pageNum = int(math.ceil(len(cards) / pagesize))
    if cards is not None:
        cardResult.nowNum = page
    if page > cardResult.pageNum:
        cardResult.cards = None
    elif page == cardResult.pageNum:
        re = cards[5 * (page - 1):len(cards)]
        cardResult.cards = re
    else:
        re = cards[5 * (page - 1):5 * page]
        cardResult.cards = re
    return cardResult


def forbiddenChange(cards: []):
    if cards is not None:
        for card in cards:
            for forbidd in forbidden:
                if forbidd['name'] == card.name:
                    card.forbidden = forbidd['status']
                    break
    return cards


def searchById(cid):
    sql = "texts.id=" + str(cid)
    # sql = "select * from texts LEFT JOIN datas on texts.id = datas.id where texts.id = {0} GROUP BY texts.name;"
    # cursor.execute(sql.format(cid))
    # cards = []
    # rows = cursor.fetchall()
    # for row in rows:
    #     card = Card(row)
    #     cards.append(card)
    # if pre_flag == 1:
    #     cursor_pre.execute(sql.format(cid))
    #     rows = cursor_pre.fetchall()
    #     for row in rows:
    #         card = Card(row)
    #         cards.append(card)
    cards = selectFS(sql)
    if extra_flag == 1:
        sql_extra = "select * from datas where id = '{0}' GROUP BY name;"
        cursor_extra.execute(sql_extra.format(cid))
        rows = cursor_extra.fetchall()
        for row in rows:
            card = Card_Extra(row)
            cards.append(card)

    return cards


def searchByName(name: str):
    org_name = copy.deepcopy(name)
    name = name.replace(" ", "")
    names = nickNameMatch(name)
    cards=[]
    print(names)
    for name in names:
        sql = "texts.name like '%{0}%'".format(name)
        cardsTemp = selectFS(sql)
        if extra_flag == 1:
            sql_extra = "select * from datas where name like '%{0}%' GROUP BY name;"
            cursor_extra.execute(sql_extra.format(name))
            rows = cursor_extra.fetchall()
            for row in rows:
                card = Card_Extra(row)
                cardsTemp.append(card)
        if len(cardsTemp) == 0:
            bg_temp = searchFromBG(org_name)
            if bg_temp is not None:
                cardsTemp = searchById(bg_temp)
        cardsTemp.sort(key=sortCard)
        cards.extend(cardsTemp)

    return cards


# 查询正式卡和先行卡
def selectFS(sql):
    sql = "select * from texts LEFT JOIN datas on texts.id = datas.id where {0} GROUP BY texts.name;".format(sql)
    cursor.execute(sql)
    cards = []
    rows = cursor.fetchall()
    for row in rows:
        card = Card(row)
        cards.append(card)
    if pre_flag == 1:
        cursor_pre.execute(sql)
        rows = cursor_pre.fetchall()
        for row in rows:
            card = Card(row)
            cards.append(card)
    return cards


def sortCard(a):
    return len(a.name)


def searchFromBG(name):
    url = bg_url + name
    response = httpx.get(url)
    js = json.loads(response.text)
    if len(js["result"]) == 0:
        return None
    else:
        return js['result'][0]['id']


def nickNameMatch(name: str) -> list:
    name = name.upper()
    toName = None
    if name in nick_name_0:
        return nick_name_0[name]
    for nick in nick_name_1:
        if nick['nick_name'] in name:
            name = name.replace(nick['nick_name'], "▶")
            toName = nick['name']
    namechar = []
    for i in range(len(name)):
        namechar.append(name[i])
    nameforsearch = "%".join(namechar)
    if toName is not None:
        nameforsearch = nameforsearch.replace("▶", toName)
    return [nameforsearch]

# a = SqliteUtils()
# name="访问"
# cursor.execute(
#     "select * from texts LEFT JOIN datas on texts.id = datas.id where texts.name like '%{0}%' GROUP BY texts.name;".format(name))
# re = cursor.fetchall()
# for row in re:
#     card = Card(row)
#     print(card.effect)
