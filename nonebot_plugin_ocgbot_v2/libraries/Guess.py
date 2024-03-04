from PIL.Image import Image
from typing import Dict
from pydantic import BaseModel
from nonebot_plugin_ocgbot_v2.libraries.Card import Card
from nonebot_plugin_ocgbot_v2.libraries.globalMessage import guess_diff



class GuessData(BaseModel):
    card: Card
    image: str
    time: int
    end: bool = False
    class Config:
        arbitrary_types_allowed = True


class Guess:
    User: Dict[str, GuessData] = {}

    async def start(self, uid: str, card: Card, image: Image):
        self.User[uid] = await self.guessData(card, image)

    def end(self, uid: str):
        del self.User[uid]

    async def time_minus(self, uid: str):
        self.User[uid].time -= 1

    async def guessData(self, card: Card, image: Image) -> GuessData:
        return GuessData(**{
            'card': card,
            'image': image,
            'time': guess_diff[0].get("time"),
            'end': False})
