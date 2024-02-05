from vkbottle.user import Message, UserLabeler

from functions.base_functions import search_user_id
from functions.methods import edit_messages
from models.users import Users
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixCommand
from rules.from_me import IsFromMe

chat_commands = UserLabeler()
chat_commands.auto_rules = [
    IsFromMe(),
    IsPrefixCommand()
]



@chat_commands.message(IsCommand(['добавить', 'add']))
async def remove_blacklist(message: Message):
    user_id = await search_user_id(message)
    if message.from_id == user_id:
        send_message == f"❎ Укажите пользователя, которого нужно добавить"
        return await edit_messages(message, send_message)
    try:
        add = await message.ctx_api.messages.add_chat_user(chat_id=message.chat_id, user_id=user_id)
        if add == 1: send_message = f"✅ [id{user_id}| Добавлен в чат]"
        return await edit_messages(message, send_message)
    except Exception as e:
        send_message = f"❎ Произошла ошибка:\n{e}"
        return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['kick', 'кик']))
async def remove_from_chat(message: Message):
    info = await Users.filter(user_id=message.from_id).first()
    if info.subscriber == 'vip' or info.subscriber == 'gold':
        user_id = await search_user_id(message)

        try:
            if message.from_id == user_id:
                send_message = 'Пока-пока.'
                await edit_messages(message, send_message)
                return await message.ctx_api.messages.remove_chat_user(chat_id=message.peer_id, user_id=user_id)

            if user_id < 0:
                remove = await message.ctx_api.messages.remove_chat_user(chat_id=message.peer_id, member_id=user_id)
                send_message = f"✅ Сообщество удалено из чата."

            else:
                remove = await message.ctx_api.messages.remove_chat_user(chat_id=message.chat_id, member_id=user_id)
                send_message = f"✅ [id{user_id}| Удален из чата.]"

            if remove == 1: return await edit_messages(message, send_message)
        except Exception as e:
            send_message = f"❎ Произошла ошибка:\n{e}"
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['дд', 'dd']))
async def user_delete_messages(message: Message):
    count = 2
    del_count = 0
    message_ids = []

    if len(message.text.split()) > 2:
        count = int(message.text.split()[2])+1

    history = await message.ctx_api.messages.get_history(
        peer_id=message.peer_id)

    for item in history.items:
        if del_count >= count: break
        if item.from_id == message.from_id:
            message_ids.append(item.id)
            del_count += 1

    await message.ctx_api.messages.delete(message_ids=message_ids, delete_for_all=1)


@chat_commands.message(IsCommand(['закрепить', 'pin']))
async def pin_message(message: Message):
    info = await Users.filter(user_id=message.from_id).first()
    if info.subscriber == 'vip' or info.subscriber == 'gold':
        if not message.reply_message.message_id:
            send_message = f'✅ Укажите сообщение, которое нужно закрепить.'
            return await edit_messages(message, send_message)

        await message.ctx_api.messages.pin(peer_id=message.peer_id,
                                           conversation_message_id=message.conversation_message_id)
        send_message = f'✅ Успешно закреплено.'
        return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['открепить', 'unpin']))
async def unpin_message(message: Message):
    info = await Users.filter(user_id=message.from_id).first()
    if info.subscriber == 'vip' or info.subscriber == 'gold':
        try:
            unpin = await message.ctx_api.messages.unpin(peer_id=message.peer_id)
            if unpin == 1:
                send_message = f'✅ Успешно откреплено.'
                return await edit_messages(message, send_message)
            else:
                send_message = f'❎ Ошибка.'
                return await edit_messages(message, send_message)
        except:
            send_message = f'❎ Для выполнения данной команды вы должны иметь право закреплять сообщения в текущем чате.'
            return await edit_messages(message, send_message)
    send_message = f"❎ Эта команда доступна минимум с подписки VIP"
    return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['+адм', '+adm']))
async def get_role_in_chat(message: Message):
    try:
        user_id = await search_user_id(message)
        await message.ctx_api.request('messages.setMemberRole', {'peer_id': message.peer_id, 'member_id': user_id, 'role': 'admin'})
        send_message = f'✅ [id{user_id}|Пользователь] повышен до админа.'
        return await edit_messages(message, send_message)
    except Exception as e:
        send_message = f"❎ Произошла ошибка.\n{e}"
        return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['-adm', '-адм']))
async def remove_role_in_chat(message: Message):
    try:
        user_id = await search_user_id(message)
        await message.ctx_api.request('messages.setMemberRole', {'peer_id': message.peer_id, 'member_id': user_id, 'role': 'member'})
        send_message = f'✅ [id{user_id}|Пользователь] снят с админа.'
        return await edit_messages(message, send_message)
    except Exception as e:
        send_message = f"❎ Произошла ошибка.\n{e}"
        return await edit_messages(message, send_message)


@chat_commands.message(IsCommand(['лс', 'ls']))
async def ls_send(message: Message):
    text = message.text.split('\n') if message.text.split('\n') >= 2 else None
    user_id = await search_user_id(message)
    if text is None:
        send_message = f"❎ Сообщение не найдено."
        return await edit_messages(message, send_message)
    try:
        await message.answer("Пиздп")
        await message.ctx_api.messages.send(user_id=user_id, message=text[1], random_id=0)
        send_message = f"[id{user_id}|✅] Сообщение отправлено."
        return await edit_messages(message, send_message)
    except Exception as e:
        send_message = f"❎ Произошла ошибка.\n{e}"
        return await edit_messages(message, send_message)
