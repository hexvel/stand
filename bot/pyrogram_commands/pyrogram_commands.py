from pyrogram import Client, filters
from pyrogram.types import Message
from models.users import Users
from vkbottle import API
from ast import literal_eval
from user.controller import UserController
from config import ProjectVariables


@Client.on_message(filters.command("start", prefixes='/'))
async def get_help(client, message: Message):
    send_message = ('Приветствуем Вас дорогой пользователь\n'
                    'Для работы нашего проекта необходимо пройти авторизацию с помощью команд:\n'
                    '1. Команда /login (ваш токен VkAdmin\n'
                    '2. Команда /restart позволяет перезапускать бота в случае зависания\n'
                    'Мы приносим извинения, так как версия 4.0 BETA')

    await client.send_message(chat_id=message.chat.id, text=send_message)


@Client.on_message(filters.command("login", prefixes='/'))
async def login(client, message: Message):
    text = message.text.split(' ')
    if len(text) >= 2:
        token_full = text[1]
        try:
            token = token_full.split('=')[1].split('&')[0]
            user = API(token)
            account = await user.account.get_profile_info()
        except:
            return await client.send_message(chat_id=message.chat.id, text='Токен инвалид или не правильно введен.')

        objects = await Users.filter(user_id=account.id).first()

        if objects is None:
            await Users.create(user_id=account.id, tg_id=message.from_user.id, token=token)
            ProjectVariables.USERS[user.user_id] = UserController(account.id)
            ProjectVariables.USERS[user.user_id].init()
            ProjectVariables.USERS[user.user_id].start()
            return await client.send_message(chat_id=message.chat.id, text='Вы зарегестрированы.')
        await Users.filter(user_id=account.id).update(token=token, tg_id=message.from_user.id)
        return await client.send_message(chat_id=message.chat.id, text='Токен обновлен.')


@Client.on_message(filters.command("restart", prefixes='/'))
async def restart_user(client, message: Message):
    get_db = await Users.filter(tg_id=message.from_user.id).first()
    if get_db is None:
        return await client.send_message(chat_id=message.chat.id, text='Не найден в базе данных.')
    user_id = literal_eval(get_db.user_id)
    if user_id != 0:
        user = UserController(get_db)
        user.restart()
        return await client.send_message(chat_id=message.chat.id, text='Session Restarted')
    return await client.send_message(chat_id=message.chat.id, text='Не найден аккаунт.')


@Client.on_message(filters.command("stop", prefixes='/'))
async def stop_user(client, message: Message):
    get_db = await Users.filter(tg_id=message.from_user.id).first()
    if get_db is None:
        return await client.send_message(chat_id=message.chat.id, text='Не найден в базе данных.')
    user_id = literal_eval(get_db.user_id)
    if user_id != 0:
        user = UserController(get_db)
        user.stop()
        return await client.send_message(chat_id=message.chat.id, text='Session Stoped')
    return await client.send_message(chat_id=message.chat.id, text='Не найден аккаунт.')

@Client.on_message(filters.command("start", prefixes='/'))
async def stop_user(client, message: Message):
    get_db = await Users.filter(tg_id=message.from_user.id).first()
    if get_db is None:
        return await client.send_message(chat_id=message.chat.id, text='Не найден в базе данных.')
    user_id = literal_eval(get_db.user_id)
    if user_id != 0:
        user = UserController(get_db)
        user.start()
        return await client.send_message(chat_id=message.chat.id, text='Session Started')
    return await client.send_message(chat_id=message.chat.id, text='Не найден аккаунт.')