from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from asgiref.sync import sync_to_async

from tgbot.management.commands.utils.orm.get import get_all_users


class NotUser(BoundFilter):

    async def check(self, message: Message):
        users = await sync_to_async(get_all_users)()
        return message.from_user.id not in users


class IsUser(BoundFilter):

    async def check(self, message: Message):
        users = await sync_to_async(get_all_users)()
        return message.from_user.id in users

