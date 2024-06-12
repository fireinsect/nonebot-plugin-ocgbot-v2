import nonebot
from nonebot import get_plugin_config
from pydantic import BaseModel
from yarl import URL

global_config = nonebot.get_driver().config
class Config(BaseModel):
    static_path: str = ""
    use_web_pic: bool = False
    bison_outer_url: str = ""
    @property
    def outer_url(self) -> URL:
        if self.bison_outer_url:
            return URL(self.bison_outer_url)
        else:
            return URL(f"http://localhost:{global_config.port}/bison/")

config = get_plugin_config(Config)
