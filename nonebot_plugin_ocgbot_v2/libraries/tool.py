import asyncio
import random
import time

import httpx
from httpx import NetworkError
from nonebot import logger



def hash(qq: int):
    # days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
    #     time.strftime("%m", time.localtime(time.time()))) + 55
    day = int(time.strftime("%d", time.localtime(time.time()))) + 4
    month = int(time.strftime("%m", time.localtime(time.time())))
    year = int(time.strftime("%y", time.localtime(time.time())))
    days = ((day + 11) * year // month + month * 31) * (year - day + 23)
    return (days * qq) >> 8


def getRandom(num: int) -> int:
    return random.randint(1, num) % num


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(1)
    raise NetworkError(f"{url} 下载失败！请重新运行或者自行前往下载")


def save(wj_path: str, img: bytes):
    with open(wj_path, "wb") as f:  # 文件写入
        f.write(img)


async def download(base_url, folder_path, file_name):
    file_path = folder_path / file_name
    byte = await download_url(base_url + file_name)
    save(file_path, byte)
    logger.info(f"文件{file_name}下载成功")
