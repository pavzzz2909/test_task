from tgbot.models import *
from django.core.exceptions import ObjectDoesNotExist


def get_current_user(user_id):
    """ Получение данных пользователя.
    Если пользователь создан возвращает объект пользователя и объект языка используемого пользователем,
    если пользователь еще не создан в БД, возвращает None """
    try:
        user = User.objects.get(cid=user_id)
        return user
    except ObjectDoesNotExist:
        return None


def get_all_users():
    return [i.cid for i in User.objects.all()]


def get_markup_by_name(name):
    return Markup.objects.get(name=name).verbose


def get_message_by_name(name):
    return Message.objects.get(name=name).verbose




