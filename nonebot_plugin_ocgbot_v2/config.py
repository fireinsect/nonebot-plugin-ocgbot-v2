from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config:
    def __init__(self):
        driver_config = get_driver().config
        try:
            self.static_path = driver_config.static_path
        except:
            self.static_path = ""

        try:
            self.use_web_pic = driver_config.use_web_pic
        except:
            self.use_web_pic = False


config = Config()
