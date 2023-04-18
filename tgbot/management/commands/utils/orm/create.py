from django.core.exceptions import ObjectDoesNotExist

from tgbot.models import User, UserAction


def create_or_update_user(message, args=None):
    model = {'cid': message.from_user.id,
             'username': message.from_user.username,
             'name': message.from_user.first_name,
             'lastname': message.from_user.last_name}
    if args:
        for key in args.keys():
            model[key] = args[key]
    return User.objects.filter(cid=message.from_user.id).update_or_create(model)


def create_user_action(user, action, dop=None):
    if dop:
        return UserAction.objects.create(cid=user, name=action, dop=dop)
    else:
        return UserAction.objects.create(cid=user, name=action)
