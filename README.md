<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ocgbot-v2

_✨ 提供游戏王相关服务 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fireinsect/nonebot-plugin-ocgbot-v2.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ocgbot-v2">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ocgbot-v2.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

提供包括查卡、随机抽卡、猜卡等功能的插件



## 📖 介绍

本插件提供了游戏王相关的服务，包括但不限于查卡、随机一卡、猜卡、查卡价、查饼图、查卡运等

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ocgbot-v2

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ocgbot-v2
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-ocgbot-v2
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-ocgbot-v2
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-ocgbot-v2
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ocgbot_v2"]

</details>

## ⚙️ 配置

在项目的`.env`文件中添加下表中的必填配置

|     配置项     | 必填 | 默认值 | 说明 |
|:-----------:|:--:|:----:|:----:|
| STATIC_PATH |  否  | 存在 | static文件夹路径，用于存放静态文件 |
|    SUPERUSERS     |  否 | 无 | 超管账号，为字符串数组 |

在项目的`static`文件夹中放入以下文件

|     文件名     | 必须 | 路径 | 说明 |
|:-----------:|:--:|:----:|:----:|
| cards.cdb |  是  | /cdb | ygo游戏文件夹下的cdb文件，拖入即可 |
|    pics     |  是 | /pics | ygo游戏文件夹下的pics文件夹，之间拖入同名文件夹即可(先行卡和自定义卡也一样) |
| daily_card.json |  是  | /json | 卡运信息，默认存在 |
| nickname.json |  是  | /json | 别名信息，默认存在 |
| pre-release.cdb |  否  | /cdb | ygo先行服的同名cdb文件 |
| extra_card.cdb |  否  | /cdb | 自定义卡牌文件，默认存在 |
## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:--:|:----:|:----:|:----:|:----:|
| help | 群员 | 否 | 群聊/私聊 | 查询功能清单 |
|查卡 ygo卡名 (页码)  | 群员 | 否 | 私聊/群聊 | 查询对应卡牌~|
| 今日卡运 | 群员 | 否 | 群聊/私聊 | 查询今日运势 |
| 随机一卡(抽一张卡) | 群员 | 否 | 群聊/私聊 | 随机一卡 |
| 猜一张卡 | 群员 | 否 | 群聊 | 随机猜一张卡 |
| 价格查询 卡名 (页码) | 群员 | 否 | 群聊/私聊 | 从集换社中查询卡牌价格 |
| 查询饼图 | 群员 | 否 | 群聊/私聊 | 从萌卡中查询卡组使用饼图 |
| 抽卡(猜卡)功能 on/off | 管理/群主/超管 | 否 | 群聊 | 开/关抽卡功能 |
| 抽卡(猜卡)cd (数字) | 管理/群主/超管 | 否 | 群聊 | 设置抽卡cd |
| 查卡方式 1/2/3 | 群员 | 否 | 群聊 | 设置查卡结果输出方式 |
| 更新禁卡表 | 超管 | 否 | 群聊/私聊 | 从官网更新最新禁卡表信息 |

## 效果图
<details>
    <summary><b>帮助菜单</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/help.png">
</details>
<details>
    <summary><b>卡牌查询</b></summary>
    <details>
        <summary>直接查询</summary>
        <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/ck1.png">
    </details>
    <details>
        <summary>输入数字选择具体查询</summary>
        <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/ck2.png">
    </details>
    <details>
        <summary>翻页</summary>
        <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/ck3.png">
    </details>
</details>
<details>
    <summary><b>查询卡运</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/kayun.png">
</details>
<details>
    <summary><b>随机一卡</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/chouk.png">
</details>
<details>
    <summary><b>随机猜卡</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/caik.png">
</details><details>
    <summary><b>查询卡价</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/jg.png">

</details>
<details>
    <summary><b>帮助菜单</b></summary>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/bt.png"> 
</details>
<details>
    <summary><b>查卡方式</b></summary>
    <h6>方式1</h6>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/chang1.png">
    <br/>    
    <h6>方式2</h6>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/change2.png">
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/change2-1.png"> 
<br/>        
    <h6>方式3</h6>
    <img src="https://raw.githubusercontent.com/fireinsect/imageSave/master/bot_img/change3.png">

</details>


