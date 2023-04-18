from aiogram import Dispatcher
from .users_filters import *


def setup(dp: Dispatcher):
    dp.filters_factory.bind(NotUser, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(IsUser, event_handlers=[dp.message_handlers])



