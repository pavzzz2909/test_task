from asgiref.sync import sync_to_async

from ..loader import bot
from ..utils.orm import get_current_user, create_user_action, create_or_update_user


async def get_user_check(from_user, message, name_of_stage, param=None):
    user = await sync_to_async(get_current_user)(from_user.id)
    await sync_to_async(create_or_update_user)(message=message)
    try:
        await bot.delete_message(chat_id=from_user.id, message_id=message.message_id - 1)
    except:
        print('No delete')
    try:
        await bot.delete_message(chat_id=from_user.id, message_id=message.message_id)
    except:
        print('No delete')
    # добавление действия пользователя
    if param:
        await sync_to_async(create_user_action)(user=user, action=name_of_stage, dop=param)
    else:
        await sync_to_async(create_user_action)(user=user, action=name_of_stage)

    return user
