from datetime import datetime
from django.core.management.base import BaseCommand

from aiogram import executor

from .loader import dp, bot, logger
from . import filters


async def on_startup(dp):
    bot_info = await bot.get_me()
    print(f'{datetime.now()}  {bot_info["first_name"]}, username: {bot_info["username"]}')


class Command(BaseCommand):
    help = 'Телеграмм Бот'

    def add_arguments(self, parser):
        parser.add_argument('--use-polling', action='store_true')

    def handle(self, *args, **kwargs):
        print('')
        print('')
        print('===========================================================================================')
        from .handlers import dp
        filters.setup(dp)

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
