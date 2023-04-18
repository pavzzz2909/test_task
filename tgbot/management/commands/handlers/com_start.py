from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from ._markups import user_main_menu_markup
from ._users_check import get_user_check

from ..filters import IsUser, NotUser
from ..loader import dp
from ..utils import create_or_update_user, create_user_action, get_message_by_name


@dp.message_handler(NotUser(), state='*')
async def cmd_start(message: Message, state: FSMContext):
    """ Если пользователя нет в БД """
    await state.finish()
    user, created = await sync_to_async(create_or_update_user)(message)
    await sync_to_async(create_user_action)(user, 'Первое обращение к боту')
    text = await sync_to_async(get_message_by_name)('hello_message')
    if message.from_user.last_name:
        text = text.replace('{last_name}', f'{message.from_user.last_name}')
    else:
        text = text.replace('{last_name}', '')
    if message.from_user.first_name:
        text = text.replace('{first_name}', f'{message.from_user.first_name}')
    else:
        text = text.replace('{first_name}', '')
    text = text.replace('{id_tg}', f'{message.from_user.id}')
    markup = await sync_to_async(user_main_menu_markup)()
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(IsUser(), commands='start', state='*')
async def cmd_start_admin(message: Message, state: FSMContext):
    await state.finish()
    user = await get_user_check(from_user=message.from_user,
                                message=message,
                                name_of_stage='Нажатие кнопки старт или ввод команды /start')
    text = await sync_to_async(get_message_by_name)('hello_message')
    if message.from_user.last_name:
        text = text.replace('{last_name}', f'{message.from_user.last_name}')
    else:
        text = text.replace('{last_name}', '')
    if message.from_user.first_name:
        text = text.replace('{first_name}', f'{message.from_user.first_name}')
    else:
        text = text.replace('{first_name}', '')
    text = text.replace('{id_tg}', f'{message.from_user.id}')
    markup = await sync_to_async(user_main_menu_markup)()
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(IsUser(), lambda query: query.data == 'back_to_start', state='*')
async def cmd_start_admin(query: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage='Переход по кнопке назад')
    text = await sync_to_async(get_message_by_name)('hello_message')
    if query.from_user.last_name:
        text = text.replace('{last_name}', f'{query.from_user.last_name}')
    else:
        text = text.replace('{last_name}', '')
    if query.from_user.first_name:
        text = text.replace('{first_name}', f'{query.from_user.first_name}')
    else:
        text = text.replace('{first_name}', '')
    text = text.replace('{id_tg}', f'{query.from_user.id}')
    markup = await sync_to_async(user_main_menu_markup)()
    await query.message.answer(text=text, reply_markup=markup)

