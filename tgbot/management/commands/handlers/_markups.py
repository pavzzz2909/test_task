from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..utils.api_moex import list_currencies
from ..utils.orm import *


def user_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    convert_currency = get_markup_by_name('convert_currency')
    view_weather = get_markup_by_name('view_weather')
    random_pic = get_markup_by_name('random_pic')
    new_polls = get_markup_by_name('new_polls')
    markup.add(InlineKeyboardButton(convert_currency, callback_data=f'convert_currency'),
               InlineKeyboardButton(view_weather, callback_data=f'view_weather'))
    markup.add(InlineKeyboardButton(random_pic, callback_data=f'random_pic'),
               InlineKeyboardButton(new_polls, callback_data=f'new_polls'))
    return markup


def back_to_start():
    markup = InlineKeyboardMarkup(row_width=1)
    button = get_markup_by_name('back_to_start')
    markup.add(InlineKeyboardButton(button, callback_data=f'back_to_start'))
    return markup


def currency_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    for key in list_currencies.keys():
        markup.add(InlineKeyboardButton(list_currencies[key], callback_data=f'currency|{key}'))
    button = get_markup_by_name('back_to_start')
    markup.add(InlineKeyboardButton(button, callback_data=f'back_to_start'))
    return markup



