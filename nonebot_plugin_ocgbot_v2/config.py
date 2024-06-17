
from nonebot import get_plugin_config
from pydantic import BaseModel



class Config(BaseModel):
    static_path: str = ""
    use_web_pic: bool = False


config = get_plugin_config(Config)
