from aiogram.dispatcher.filters.state import StatesGroup, State


class City(StatesGroup):
    city = State()


class Currency(StatesGroup):
    c_from = State()
    count = State()


class New_Polls(StatesGroup):
    id_tg = State()
    question = State()
    options = State()


