from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async


from ._markups import back_to_start
from ._states import *
from ._users_check import get_user_check

from ..utils.api_weather import ApiWeather
from ..filters import IsUser
from ..loader import dp
from ..utils import get_message_by_name


@dp.callback_query_handler(IsUser(), lambda query: query.data == 'view_weather', state='*')
async def management(query: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage='Переход по кнопке прогноза погоды')
    text = await sync_to_async(get_message_by_name)('view_weather_enter_city')
    markup = await sync_to_async(back_to_start)()
    await query.message.answer(text=text, reply_markup=markup)
    await City.city.set()


@dp.message_handler(IsUser(), state=City.city)
async def cmd_start_admin(message: Message, state: FSMContext):
    city = message.text
    data = ApiWeather().get_weather(city)
    if 'message' in data.keys():
        text = await sync_to_async(get_message_by_name)('view_weather_resp_error')
        text = text.replace('{error}', f"{data['message']}")
        markup = await sync_to_async(back_to_start)()
        user = await get_user_check(from_user=message.from_user,
                                    message=message,
                                    name_of_stage='Ответ сервера погоды',
                                    param=f'Ошибка {data}')
        await message.answer(text=text, reply_markup=markup)
    else:
        text = await sync_to_async(get_message_by_name)('view_weather_resp')
        markup = await sync_to_async(back_to_start)()
        text = text.replace('{city}', f"{data['name']}")\
                   .replace('{weather_description}', f"{data['weather'][0]['description']}")\
                   .replace('{temp}', f"{data['main']['temp']}")\
                   .replace('{temp_feels_like}', f"{data['main']['feels_like']}")\
                   .replace('{wind}', f"{data['wind']['speed']}")
        user = await get_user_check(from_user=message.from_user,
                                    message=message,
                                    name_of_stage='Ответ сервера погоды',
                                    param=f'{data}')
        await message.answer(text=text, reply_markup=markup)
        await state.finish()
