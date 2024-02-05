from models.users import Users
from rules.from_me import IsFromMe
from rules.check_prefix import IsPrefixCommand
from rules.check_command import IsCommand
from vkbottle.user import Message, UserLabeler
from functions.base_functions import search_user_id
from functions.methods import edit_messages


list_commands = UserLabeler()
list_commands.auto_rules = [
    IsFromMe(),
    IsPrefixCommand()
]


@list_commands.message(IsCommand(['+игнор', '+ignore']))
async def add_ignore(message: Message):
    get_db = await Users.filter(user_id=message.from_id).first()
    if get_db.subscriber == 'vip' or get_db.subscriber == 'gold':
        user_id = await search_user_id(message)

        if message.from_id == user_id:
            send_message = "❎ Укажите пользователя, которого нужно добавить."
            return await edit_messages(message, send_message)
        try:
            list_ignore = get_db.ignore_list
            if user_id in list_ignore:
                send_message = f"❎ [id{user_id}| Уже есть в игнор листе.]"
                return await edit_messages(message, send_message)
            list_ignore.append(user_id)
            await Users.filter(user_id=message.from_id).update(ignore_list=list_ignore)

            send_message = f"✅ [id{user_id}| Добавлен в игнор.]"
            return await edit_messages(message, send_message)
        except Exception as e:
            send_message = f"❎ Произошла ошибка.\n{e}"
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)

@list_commands.message(IsCommand(['-игнор', '-ignore']))
async def remove_ignore(message: Message):
    get_db = await Users.filter(user_id=message.from_id).first()
    if get_db.subscriber == 'vip' or get_db.subscriber == 'gold':
        user_id = await search_user_id(message)
        if message.from_id == user_id:
            send_message = "❎ Укажите пользователя, которого нужно убрать из игнор листа."
            return await edit_messages(message, send_message)
        try:
            list_ignore = get_db.ignore_list
            if user_id in list_ignore:
                list_ignore.remove(user_id)
                await Users.filter(user_id=message.from_id).update(ignore_list=list_ignore)
                send_message = f"✅ [id{user_id}| Удален из игнор листа.]"
                return await edit_messages(message, send_message)
            send_message = f"❎ [id{user_id}| Не найден в игнор листе.]"
            return await edit_messages(message, send_message)
        except Exception as e:
            send_message = f"❎ Произошла ошибка.\n{e}"
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@list_commands.message(IsCommand(['игнор', 'ignor']))
async def list_ignore(message: Message):
    info = await Users.filter(user_id=message.from_id).first()
    if info.subscriber == 'vip' or info.subscriber == 'gold':
        list_ignore = info.ignore_list
        if len(info.ignore_list) == 0:
            send_message = f'❎ У [id{message.from_id}|вас] пустой список игнорируемых пользователей.'
            return await edit_messages(message, send_message)
        send_message = f'✅ Игнор лист [id{message.from_id}|пользователя]:\n\n'
        for i, user in enumerate(list_ignore):
            user_get = await message.ctx_api.users.get(user_ids=user)
            name, fam = user_get[0].first_name, user_get[0].last_name
            send_message += '{}. [id{}|{} {}]\n'.format(i+1, user, name, fam)
        return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@list_commands.message(IsCommand(['+дов', '+dov']))
async def add_trust(message: Message):
    get_db = await Users.filter(user_id=message.from_id).first()
    if get_db.subscriber == 'vip' or get_db.subscriber == 'gold':
        user_id = await search_user_id(message)

        if message.from_id == user_id:
            send_message = "❎ Укажите пользователя, которого нужно добавить."
            return await edit_messages(message, send_message)
        try:
            list_trust = get_db.trust_list
            if user_id in list_trust:
                send_message = f"❎ [id{user_id}| Уже есть в доверенных.]"
                return await edit_messages(message, send_message)
            list_trust.append(user_id)
            await Users.filter(user_id=message.from_id).update(trust_list=list_trust)
            send_message = f"✅ [id{user_id}| Добавлен в доверенные.]"
            return await edit_messages(message, send_message)
        except Exception as e:
            send_message = f"❎ Произошла ошибка.\n{e}"
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@list_commands.message(IsCommand(['-дов', '-dov']))
async def remove_trust(message: Message):
    get_db = await Users.filter(user_id=message.from_id).first()
    if get_db.subscriber == 'vip' or get_db.subscriber == 'gold':
        user_id = await search_user_id(message)
        if message.from_id == user_id:
            send_message = "❎ Укажите пользователя, которого нужно убрать из доверенных."
            return await edit_messages(message, send_message)
        try:
            list_trust = get_db.trust_list
            if user_id in list_trust:
                list_trust.remove(user_id)
                await Users.filter(user_id=message.from_id).update(trust_list=list_trust)
                send_message = f"✅ [id{user_id}| Удален из доверенных.]"
                return await edit_messages(message, send_message)
            send_message = f"❎ [id{user_id}| Не найден в доверенных.]"
            return await edit_messages(message, send_message)
        except Exception as e:
            send_message = f"❎ Произошла ошибка.\n{e}"
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@list_commands.message(IsCommand(['довы', 'dov']))
async def list_ignore(message: Message):
    info = await Users.filter(user_id=message.from_id).first()
    if info.subscriber == 'vip' or info.subscriber == 'gold':
        list_trust = info.trust_list
        if len(info.trust_list) == 0:
            send_message = f'❎ У [id{message.from_id}|вас] пустой список игнорируемых пользователей.'
            return await edit_messages(message, send_message)
        send_message = f'✅ Доверенные [id{message.from_id}|пользователи]:\n\n'
        for i, user in enumerate(list_trust):
            user_get = await message.ctx_api.users.get(user_ids=user)
            name, fam = user_get[0].first_name, user_get[0].last_name
            send_message += '{}. [id{}|{} {}]\n'.format(i+1, user, name, fam)
        return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)
