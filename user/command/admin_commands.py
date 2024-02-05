import subprocess

from vkbottle import API
from vkbottle.user import Message, UserLabeler

from functions.base_functions import search_user_id
from functions.methods import edit_messages
from models.users import Users, Scripts
from utils.query import Request

from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixAdmin
from rules.from_me import IsFromMe

from config import ProjectVariables

admin_command = UserLabeler()
admin_command.auto_rules = [IsFromMe(), IsPrefixAdmin()]


@admin_command.message(IsCommand(["reg", "рег"]))
async def registation(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if message.reply_message:
        text = message.reply_message.text

    if db_owner.user_rank < 2 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)
    try:
        token = text.split("=")[1].split("&")[0]
        user = API(token)
        account = await user.account.get_profile_info()
    except:
        send_message = "⚠ токен не правильный или невалид."
        return await edit_messages(message, send_message)

    if db_user is not None:
        await Users.filter(user_id=account.id).update(token=token)
        send_message = "✅ [id{}|Updated.]".format(user_id)
        return await edit_messages(message, send_message)

    if db_user is None:
        await Scripts.create(user_id=user_id)
        await Users.create(user_id=user_id, token=token)
        await Request.request("http://127.0.0.1:3000/api/create", data={"user_id": user_id})

        send_message = "✅ [id{}|Successfully create new user.]".format(user_id)
        return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["+vip", "+вип"]))
async def get_vip(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 3 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своей подпиской."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять подпиской выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if db_user.subscriber == "gold":
        send_message = "👑 пользователь уже имеет GOLD."
        return await edit_messages(message, send_message)

    if db_user.subscriber == "vip":
        send_message = "💎 пользователь уже имеет VIP."
        return await edit_messages(message, send_message)

    await Users.filter(user_id=user_id).update(subscriber="vip")
    send_message = "💎 [id{}|пользователь] получил VIP.".format(user_id)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["+gold", "+голд"]))
async def get_gold(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своей подпиской."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять подпиской выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if db_user.subscriber == "gold":
        send_message = "👑 пользователь уже имеет GOLD."
        return await edit_messages(message, send_message)

    await Users.filter(user_id=user_id).update(subscriber="gold")
    send_message = "👑 [id{}|пользователь] получил GOLD.".format(user_id)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["-sub", "-подписка"]))
async def remove_sub(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своей подпиской."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять подпиской выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if db_user.subscriber == "free":
        send_message = "⚠ у пользоватея неетподписки."
        return await edit_messages(message, send_message)

    await Users.filter(user_id=user_id).update(subscriber="free")
    send_message = "✅ [id{}|пользователь]те ерь без подписки.".format(user_id)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["+баланс", "+печеньки"]))
async def add_balance(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()
    text = message.text.split("\n")

    if db_owner.user_rank < 4 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if len(text) < 2:
        send_message = "⚠ не указано количество печенек."
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своим балансом."
        return await edit_messages(message, send_message)

    try:
        kol = int(text[1])
    except:
        send_message = "⚠ неправильно указано количество."
        return await edit_messages(message, send_message)

    balance = db_user.balance
    await Users.filter(user_id=user_id).update(balance=balance + kol)
    send_message = "✅ [id{}|пользователю] начислено {} печенек.".format(user_id, kol)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["-баланс", "-печеньки"]))
async def nul_balance(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять балансом выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своим балансом."
        return await edit_messages(message, send_message)

    if db_user.balance == 0:
        send_message = "⚠ нельзя обнулять нулевой баланс."
        return await edit_messages(message, send_message)

    await Users.filter(user_id=user_id).update(balance=0)
    send_message = "✅ [id{}|пользователю] обнулено количнство печенек.".format(user_id)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["повысить"]))
async def add_rank(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4 and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять рангом выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своим рангом."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= 5:
        send_message = "⚠ у пользователя максимальный ранг."
        return await edit_messages(message, send_message)

    rank = db_user.user_rank
    await Users.filter(user_id=user_id).update(user_rank=rank + 1)
    new_rank = {
        1: "пользователем",
        2: "агентом",
        3: "модератором",
        4: "админом",
        5: "главным",
    }[rank + 1]
    send_message = "✅ [id{}|пользователь] назначен {}.".format(user_id, new_rank)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["понизить"]))
async def del_rank(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять рангом выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своим рангом."
        return await edit_messages(message, send_message)

    if db_user.user_rank <= 1:
        send_message = "⚠ у пользователя минимальный ранг."
        return await edit_messages(message, send_message)

    rank = db_user.user_rank
    await Users.filter(user_id=user_id).update(user_rank=rank - 1)
    new_rank = {
        1: "пользователем",
        2: "агентом",
        3: "модератором",
        4: "админом",
        5: "главным",
    }[rank + 1]
    send_message = "✅ [id{}|пользователь] назначен {}.".format(user_id, new_rank)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["снять"]))
async def nul_rank(message: Message):
    user_id = await search_user_id(message)
    db_user = await Users.filter(user_id=user_id).first()
    db_owner = await Users.filter(user_id=message.from_id).first()

    if db_owner.user_rank < 4:
        send_message = "⚠ недостаточно прав."
        return await edit_messages(message, send_message)

    if db_user is None:
        send_message = "⚠ не найден в базе данных."
        return await edit_messages(message, send_message)

    if db_user.user_rank >= db_owner.user_rank and message.from_id not in [
        3744817,
        823349848,
    ]:
        send_message = (
            "⚠ нельзя управлять рангом выше или равного по рангу пользователя."
        )
        return await edit_messages(message, send_message)

    if user_id == message.from_id and message.from_id not in [3744817, 823349848]:
        send_message = "⚠ нельзя управлять своим рангом."
        return await edit_messages(message, send_message)

    if db_user.user_rank <= 1:
        send_message = "⚠ пользователь не был админом."
        return await edit_messages(message, send_message)

    await Users.filter(user_id=user_id).update(user_rank=1)
    send_message = "✅ [id{}|пользователь] назначен пользователем.".format(user_id)
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["чек"]))
async def check_user_session(message: Message):
    user_id = await search_user_id(message)
    db_owner = await Users.filter(user_id=message.from_id).first()
    
    if db_owner.user_rank < 2:
    	s_message = "⚠ недостаточно прав."
    	return await edit_messages(message, s_message)

    if user_id == message.from_id:
        send_message = "⚠ укажите пользователя."
        return await edit_messages(message, send_message)
    
    send_message = f"🔧 Статус сессии [id{user_id}|пользователя]:\n"
    
    if user_id in ProjectVariables.USERS:
        send_message += "Бот ✅\n"
    else:
        send_message += "Бот ❌\n"

    if user_id in ProjectVariables.SCRIPTS:
        send_message += "Скрипты ✅\n"
    else:
        send_message += "Скрипты ❌"
    
    return await edit_messages(message, send_message)


@admin_command.message(IsCommand(["рестарт"]))
async def restart_bot(message: Message):
	db_owner = await Users.filter(user_id=message.from_id).first()
	
	if db_owner.user_rank < 4:
		s_message = "⚠ недостаточно прав."
		return await edit_messages(message, s_message)
		
	s_message = "⚡ перезапуск."
	await edit_messages(message, s_message)
	subprocess.run(["systemctl", "restart", "bot"])