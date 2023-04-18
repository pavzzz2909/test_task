from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
import requests

from ._markups import back_to_start
from ._states import *
from ._users_check import get_user_check

from ..filters import IsUser
from ..loader import dp, bot
from ..utils import (get_message_by_name)


@dp.callback_query_handler(IsUser(), lambda query: query.data == 'random_pic', state='*')
async def management(query: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage='Случайная картинка')
    try:
        resp = requests.get('http://thecatapi.com/api/images/get?format=src')
        url = resp.url
        text = await sync_to_async(get_message_by_name)('random_pic')
        markup = await sync_to_async(back_to_start)()
        await bot.send_photo(chat_id=query.from_user.id, photo=url, caption=text, reply_markup=markup)
    except:
        text = await sync_to_async(get_message_by_name)('random_pic_error')
        markup = await sync_to_async(back_to_start)()
        await query.message.answer(text=text, reply_markup=markup)

