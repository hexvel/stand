import ast
import time
from datetime import datetime

from vkbottle.user import Message, UserLabeler

from config import Emoji, ProjectVariables, ProjectData
from functions.base_functions import search_user_id
from models.users import Scripts, Users
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixCommand
from rules.from_me import IsFromMe
from utils import APIMethod

default_commands = UserLabeler()
default_commands.auto_rules = [IsFromMe(), IsPrefixCommand()]


@default_commands.message(IsCommand(["пинг", "ping"]), blocking=False)
async def ping(message: Message):
    methods = APIMethod(message)
    ping = time.time() - message.date
    send_message = f"{Emoji.WATCH} PingTime: {ping:.3f}s.".replace("-", "")
    await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["инфо", "info"]))
async def user_info(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)

    ping = time.time() - message.date

    if await Users.filter(user_id=user_id).first() is None:
        await methods.edit_messages(
            f"⚠ [id{user_id}|пользователь] не зарегестрирован в боте."
        )
        return

    rank = {1: "Пользователь", 2: "Агент", 3: "Модератор", 4: "Админ", 5: "Главный"}

    get_db = await Users.filter(user_id=user_id).first()
    get_scripts = await Scripts.filter(user_id=user_id).first()
    spam_status = "Включен" if get_scripts.spam else "Выключен"
    is_token = "✅" if get_db.token != "None" else "❎"
    now_time = datetime.now().strftime("%H:%M")
    worked_time = time.time() - ProjectData.START_TIME
    info_from_api = await message.ctx_api.users.get(user_ids=user_id)

    if get_db.info_mode == "default":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            nickname=get_db.user_name,
            spam_status=spam_status,
            role=rank[get_db.user_rank],
            time=now_time,
        )
    elif get_db.info_mode == "thisby":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            ping=f"{ping:.3f}",
            name=info_from_api[0].first_name,
            surname=info_from_api[0].last_name,
            nickname=get_db.user_name,
            role=rank[get_db.user_rank],
        )
    elif get_db.info_mode == "reid":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            role=rank[get_db.user_rank],
            prefix=get_db.prefix_commands,
            user_id=user_id,
            chat_id=message.peer_id,
            spam_status=spam_status,
            worked_time=round(worked_time)
        )
    elif get_db.info_mode == "paradox":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            role=rank[get_db.user_rank],
            prefix=get_db.prefix_commands,
            chat_id=message.peer_id,
            spam_status=spam_status,
            worked_time=round(worked_time)
        )
    elif get_db.info_mode == "hexvel":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            balance=get_db.balance,
            nickname=get_db.user_name,
            role=rank[get_db.user_rank],
            is_token=is_token,
            prefix_commands=get_db.prefix_commands,
            prefix_scripts=get_db.prefix_scripts,
            prefix_admins=get_db.prefix_admin,
            chat_id=message.peer_id,
            spam_status=spam_status,
        )
    elif get_db.info_mode == "alya":
        send_message = ProjectVariables.GET_INFO[get_db.info_mode].format(
            prefix=get_db.prefix_commands,
            time=now_time
        )

    await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["спуфер", "spoofer"]))
async def set_spoofer(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            text = message.text.split(" ", maxsplit=2)[2]

            if text not in ["default", "thisby", "reid", "paradox", "hexvel", "сбросить", "alya"]:
                await methods.edit_messages(
                    f"{Emoji.WARNING} Укажите существующую тему."
                )
                return

            if text == "сбросить":
                await Users.filter(user_id=message.from_id).update(info_mode="default")
            else:
                await Users.filter(user_id=message.from_id).update(info_mode=text)

            if text == "сбросить":
                text = "по умолчанию"
            send_message = f"✅ Тема вывода инфы обновлена на ['{text}']."
            await methods.edit_messages(send_message)
            return

        send_message = f"❎ Вы не указали название темы."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["реши", "reshi"]))
async def calc(message: Message):
    methods = APIMethod(message)
    message_split = message.text.split()

    if len(message_split) >= 5:
        num1 = int(message_split[2]) if message_split[2].isdigit() else None
        num2 = int(message_split[4]) if message_split[4].isdigit() else None
        operator = message_split[3]

        if not num1 and not num2:
            await methods.edit_messages(message, "❎ Неправильно указаны параметры.")

        if operator == "*":
            result = num1 * num2
        elif operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "/":
            result = num1 / num2
        elif operator == "%":
            result = num1 % num2
        elif operator == "**":
            result = num1**num2
        else:
            await methods.edit_messages(message, "❎ Не правильно указано действие.")
            return
        await methods.edit_messages(
            message,
            "✏ Пример: {}\n✅ Ответ: {}.".format(f"{num1}{operator}{num2}", result),
        )
    await methods.edit_messages(message, "❎ Не указан пример.")


@default_commands.message(IsCommand(["+др", "+dr"]))
async def add_friend(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)
    try:
        add = await message.ctx_api.friends.add(user_id=user_id)
        if add == 1:
            send_message = f"✅ [id{user_id}|Заявка отправлена.]"
            await methods.edit_messages(send_message)
            return
        elif add == 2:
            send_message = f"✅ [id{user_id}|Заявка одобрена.]"
            await methods.edit_messages(send_message)
            return
        elif add == 4:
            send_message = f"✅ [id{user_id}|Заявка отправлена повторно.]"
            await methods.edit_messages(send_message)
            return
    except Exception as e:
        if e.code == 174:
            send_message = f"❎ [id{user_id}| Не удается добавить.]"
        elif e.code == 175:
            send_message = f"❎ [id{user_id}| Вы в ЧС у пользователя.]"
        elif e.code == 176:
            send_message = f"❎ [id{user_id}| Пользователь у вас в ЧС.]"
        elif e.code == 177:
            send_message = f"❎ [id{user_id}| Пользователь не найден.]"
        else:
            send_message = f"❎ [id{user_id}| Неизвестная ошибка.]"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-др", "-dr"]))
async def delete_friend(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)
    try:
        delete = await message.ctx_api.friends.delete(user_id=user_id)
        if delete == "success" or "friend_deleted":
            send_message = f"✅ [id{user_id}| Пользователь удален.]"
            await methods.edit_messages(send_message)
            return
        elif delete == "out_request_deleted":
            send_message = f"✅ [id{user_id}| Заявка пользователя отклонена.]"
            await methods.edit_messages(send_message)
            return
        elif delete == "in_request_deleted":
            send_message = f"✅ [id{user_id}| Входящая заявка пользователя отклонена.]"
            await methods.edit_messages(send_message)
            return
        elif delete == "suggestion_deleted":
            send_message = f"✅ [id{user_id}| Удален из рекомендаций.]"
            await methods.edit_messages(send_message)
            return
        else:
            send_message = f"✅ [id{user_id}| Успешно.]"
            await methods.edit_messages(send_message)
            return
    except Exception as e:
        send_message = f"❎ [id{user_id}| Неизвестная ошибка.]\n{e}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["+чс", "+chs"]))
async def add_blacklist(message: Message):
    methods = APIMethod(message)

    try:
        user_id = await search_user_id(message)
        add = await message.ctx_api.account.ban(user_id=user_id)
        if add in [1, 2]:
            send_message = f"✅ [id{user_id}|Добавил в ЧС.]"
            await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-чс", "-chs"]))
async def remove_blacklist(message: Message):
    methods = APIMethod(message)

    try:
        user_id = await search_user_id(message)
        add = await message.ctx_api.account.unban(user_id=user_id)
        if add == 1:
            send_message = f"✅ [id{user_id}| Убрал из ЧС.]"
            await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["ид", "id"]))
async def get_user_id(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)
    send_message = f"✅ [id{user_id}|{user_id}]"
    await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["commands", "команды"]))
async def get_commands(message: Message):
    methods = APIMethod(message)
    send_message = "https://vk.cc/crOSja"
    await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-префикс", "-prefix"]))
async def set_prefix_commands(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            prefix = message.text.split(" ")[2]
            ProjectVariables.USERS[message.from_id].data.prefix_commands = prefix
            await Users.filter(user_id=message.from_id).update(prefix_commands=prefix)
            send_message = f"✅ Префикс команд обновлен на ['{prefix}']"
            await methods.edit_messages(send_message)
            return
        send_message = f"❎ Вы не указали префикс."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-спрефикс", "-sprefix"]))
async def set_prefix_sripts(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            prefix = message.text.split(" ")[2]
            ProjectVariables.USERS[message.from_id].data.prefix_commands = prefix
            await Users.filter(user_id=message.from_id).update(prefix_scripts=prefix)
            send_message = f"✅ Префикс скриптов обновлен на ['{prefix}']"
            await methods.edit_messages(send_message)
            return
        send_message = f"❎ Вы не указали префикс."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-ппрефикс", "-pprefix"]))
async def set_trusted_sripts(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            prefix = message.text.split(" ")[2]
            await Users.filter(user_id=message.from_id).update(trust_prefix=prefix)
            send_message = f"✅ Префикс повторялки обновлен на ['{prefix}']"
            await methods.edit_messages(send_message)
            return
        send_message = f"❎ Вы не указали префикс."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-апрефикс", "-aprefix"]))
async def set_trusted_sripts(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            prefix = message.text.split(" ")[2]
            ProjectVariables.USERS[message.from_id].data.admin_prefix = prefix
            await Users.filter(user_id=message.from_id).update(prefix_admin=prefix)
            send_message = f"✅ Префикс повторялки обновлен на ['{prefix}']"
            await methods.edit_messages(send_message)
            return
        send_message = f"❎ Вы не указали префикс."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)


@default_commands.message(IsCommand(["-ник", "-nick"]))
async def set_nick(message: Message):
    methods = APIMethod(message)

    try:
        if len(message.text.split(" ")) >= 3:
            nick = message.text.split(" ")[2]
            await Users.filter(user_id=message.from_id).update(user_name=nick)
            send_message = f"✅ Никнейм обновлен на ['{nick}']"
            await methods.edit_messages(send_message)
            return
        send_message = f"❎ Вы не указали никнейм."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)
