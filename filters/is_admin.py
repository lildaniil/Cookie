from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data import config


#filter check permissions: is user admin or not
class IsAdmin(BoundFilter):
    async def check(self, message:types.Message) -> bool:
        if str(message.from_user.id) in config.ADMINS:
            return True
        else: return False