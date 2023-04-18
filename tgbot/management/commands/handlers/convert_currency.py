from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async


from ._markups import currency_markup, back_to_start
from ._states import *
from ._users_check import get_user_check

from ..utils.api_moex import ApiMoex, list_currencies
from ..filters import IsUser
from ..loader import dp
from ..utils import get_message_by_name


@dp.callback_query_handler(IsUser(), lambda query: query.data == 'convert_currency', state='*')
async def management(query: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage='Переход по кнопке конвертация валюты')
    text = await sync_to_async(get_message_by_name)('convert_currency_from')
    markup = await sync_to_async(currency_markup)()
    await query.message.answer(text=text, reply_markup=markup)
    await Currency.c_from.set()


@dp.callback_query_handler(IsUser(), lambda query: query.data.startswith('currency'), state=Currency.c_from)
async def management(query: CallbackQuery, state: FSMContext):
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage=f'Выбор валюты {query.data.split("|")[1]}')
    async with state.proxy() as data:
        data['c_from'] = query.data.split('|')[1]
    text = await sync_to_async(get_message_by_name)('convert_currency_count')
    markup = await sync_to_async(back_to_start)()
    await query.message.answer(text=text, reply_markup=markup)
    await Currency.count.set()


@dp.message_handler(IsUser(), state=Currency.count)
async def cmd_start_admin(message: Message, state: FSMContext):
    user = await get_user_check(from_user=message.from_user,
                                message=message,
                                name_of_stage=f'Выбор количества {message.text}')
    try:
        async with state.proxy() as data:
            data['count'] = int(message.text)
        list_data = ApiMoex().get_curses()
        if data:
            for item in list_data:
                if data['c_from'] == item['SECID']:
                    name = list_currencies[data['c_from']]
                    price = item['LAST']
            summ = round(price*data['count'], 2)
            text = await sync_to_async(get_message_by_name)('converted_currencies')
            text = text.replace('{count_from}', f'{name}')\
                       .replace('{val_from}', f"{data['count']}")\
                       .replace('{count_to}', f'{summ}')
        else:
            text = await sync_to_async(get_message_by_name)('converted_currencies_error')
        markup = await sync_to_async(back_to_start)()
        await message.answer(text=text, reply_markup=markup)
        await state.finish()
    except:
        text = await sync_to_async(get_message_by_name)('convert_currency_count_error')
        markup = await sync_to_async(back_to_start)()
        await message.answer(text=text, reply_markup=markup)
