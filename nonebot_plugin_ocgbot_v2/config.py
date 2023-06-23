from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    static_path: str = "nonebot_plugin_ocgbot_v2/static/"
