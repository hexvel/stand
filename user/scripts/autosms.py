from vkbottle.user import Message, UserLabeler

from config import Emoji
from utils import APIMethod
from models.users import Scripts

from rules.from_me import IsFromMe
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixScript

from functions.base_functions import search_user_id

autosms_scripts = UserLabeler()
autosms_scripts.auto_rules = [IsPrefixScript(), IsFromMe()]


@autosms_scripts.message(IsCommand(["+автосмс", "+autosms"]))
async def start_autosms(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)
    user_data = await Scripts.filter(user_id=message.from_id).first()

    if user_id == message.from_id:
        await methods.edit_messages(f"{Emoji.WARNING} Укажите пользователя.")
        return

    if user_data.auto_sms and user_id in user_data.auto_sms_users['users']:
        await methods.edit_messages(f"{Emoji.NO} Автосмс уже включён.")
        return

    user_data.auto_sms_users['users'].append(user_id)

    await Scripts.filter(user_id=message.from_id).update(
        auto_sms=True,
        auto_sms_users=dict(users=user_data.auto_sms_users['users'])
    )

    await message.ctx_api.messages.delete(
        peer_id=message.peer_id,
        message_ids=message.id,
        delete_for_all=1
    )


@autosms_scripts.message(IsCommand(["-автосмс", "-autosms"]))
async def start_autosms(message: Message):
    methods = APIMethod(message)
    user_id = await search_user_id(message)

    user_data = await Scripts.filter(user_id=message.from_id).first()

    if not user_data.auto_sms or user_id not in user_data.auto_sms_users['users']:
        await methods.edit_messages(f"{Emoji.NO} Автосмс уже выключен.")
        return

    user_data.auto_sms_users['users'].remove(user_id)

    await Scripts.filter(user_id=message.from_id).update(
        auto_sms=True,
        auto_sms_users=dict(users=user_data.auto_sms_users['users'])
    )

    await message.ctx_api.messages.delete(
        peer_id=message.peer_id,
        message_ids=message.id,
        delete_for_all=1
    )


@autosms_scripts.message(IsCommand(["автосмс", "autosms"]))
async def start_autosms(message: Message):
    methods = APIMethod(message)
    try:
        if len(message.text.split(" ")) >= 3:
            text = message.text.split(" ", maxsplit=2)[2]
            await Scripts.filter(user_id=message.from_id).update(auto_sms_text=text)
            send_message = f"✅ Текст автосмс обновлен на ['{text}']."
            await methods.edit_messages(send_message)
            return

        send_message = f"❎ Вы не указали Текст."
        await methods.edit_messages(send_message)
    except Exception as ex:
        send_message = f"❎ Произошла ошибка:\n{ex}"
        await methods.edit_messages(send_message)
