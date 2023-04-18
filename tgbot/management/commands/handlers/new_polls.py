from aiogram.types import CallbackQuery, Message, PollAnswer, ChatType
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async

from ._markups import *
from ._states import *
from ._users_check import get_user_check

from ..filters import IsUser
from ..loader import dp, bot
from ..utils import get_message_by_name


@dp.callback_query_handler(IsUser(), lambda query: query.data == 'new_polls', state='*')
async def management(query: CallbackQuery, state: FSMContext):
    user = await get_user_check(from_user=query.from_user,
                                message=query.message,
                                name_of_stage='Переход по кнопке новый опрос')
    await state.finish()
    text = await sync_to_async(get_message_by_name)('new_polls')
    markup = await sync_to_async(back_to_start)()
    await query.message.answer(text=text, reply_markup=markup)
    await New_Polls.id_tg.set()


@dp.message_handler(IsUser(), state=New_Polls.id_tg)
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user_check(from_user=message.from_user,
                                message=message,
                                name_of_stage=f'Выбор id отправки {message.text}')
    try:
        async with state.proxy() as data:
            data['id_tg'] = int(message.text)
        text = await sync_to_async(get_message_by_name)('new_polls_correct_id')
        markup = await sync_to_async(back_to_start)()
        await message.answer(text=text, reply_markup=markup)
        await New_Polls.question.set()
    except:
        text = await sync_to_async(get_message_by_name)('new_polls_id_error')
        markup = await sync_to_async(back_to_start)()
        await message.answer(text=text, reply_markup=markup)


@dp.message_handler(IsUser(), state=New_Polls.question)
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user_check(from_user=message.from_user,
                                message=message,
                                name_of_stage=f'Выбор вопроса {message.text}')
    async with state.proxy() as data:
        data['question'] = message.text
    text = await sync_to_async(get_message_by_name)('new_polls_options')
    markup = await sync_to_async(back_to_start)()
    await message.answer(text=text, reply_markup=markup)
    await New_Polls.options.set()


@dp.message_handler(IsUser(), state=New_Polls.options)
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user_check(from_user=message.from_user,
                                message=message,
                                name_of_stage=f'Выбор ответов {message.text}')
    options = message.text.split(',')
    if len(options) > 10:
        text = await sync_to_async(get_message_by_name)('new_polls_options_error')
        markup = await sync_to_async(back_to_start)()
        await message.answer(text=text, reply_markup=markup)
    else:
        async with state.proxy() as data:
            data['options'] = options
        try:
            await bot.send_poll(chat_id=data['id_tg'], question=data['question'], options=data['options'])
            text = await sync_to_async(get_message_by_name)('sending_poll')
            markup = await sync_to_async(back_to_start)()
            await message.answer(text=text, reply_markup=markup)
        except:
            text = await sync_to_async(get_message_by_name)('sending_poll_error')
            markup = await sync_to_async(back_to_start)()
            await message.answer(text=text, reply_markup=markup)
