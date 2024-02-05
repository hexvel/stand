from vkbottle.user import Message, UserLabeler

from config import Emoji, ProjectVariables
from models.users import Scripts, Spam, Users
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixScript
from rules.from_me import IsFromMe
from utils import APIMethod

spam = UserLabeler()
spam.auto_rules = [IsFromMe(), IsPrefixScript()]


def is_number(_str: str):
    try:
        float(_str)
        return True
    except ValueError:
        return False


@spam.message(IsCommand(["+спам", "+spam"]))
async def stop_spam(message: Message):
    methods = APIMethod(message)
    data = await Users.filter(user_id=message.from_id).first()

    message_split = message.text.split(maxsplit=3)
    attachments = [None]

    if len(message_split) < 4:
        await methods.edit_messages("❎ Не указаны параметры.")
        return

    sleep = message_split[2]
    text = message_split[-1]

    if not is_number(sleep):
        await methods.edit_messages("❎ Укажите задержку цифрами.")
        return

    if float(sleep) < 0.5 and data.user_rank < 4:
        await methods.edit_messages(
            "❎ Нельзя ставить задержку меньше секунды с данной подпиской."
        )
        return

    if float(sleep) < 0.3:
        await methods.edit_messages("❎ Нельзя ставить задержку меньше 0.3 сек.")
        return

    if message.attachments:
        attachments = []
        dictionary = message.attachments
        for i in range(1, len(dictionary) // 2 + 1):
            type_key = "attach{}_type".format(i)
            value_key = "attach{}".format(i)
            object_str = dictionary[type_key] + dictionary[value_key]
            attachments.append(object_str)

    if await Spam.filter(user_id=message.from_id, peer_id=message.peer_id).first():
        await Spam.filter(user_id=message.from_id, peer_id=message.peer_id).update(
            user_id=message.from_id,
            peer_id=message.peer_id,
            text=text,
            attachments=attachments,
            spam_sleep=float(sleep),
            is_active=True
        )

    else:
        await Spam.create(
            user_id=message.from_id,
            peer_id=message.peer_id,
            text=text,
            attachments=attachments,
            spam_sleep=float(sleep),
            is_active=True
        )

    await Scripts.filter(user_id=message.from_id).update(spam=True)
    await message.ctx_api.messages.delete(
        peer_id=message.peer_id,
        message_ids=message.id,
        delete_for_all=1
    )


@spam.message(IsCommand(["-спам", "-spam"]))
async def stop_spam(message: Message):
    methods = APIMethod(message)

    user_data = await Scripts.filter(user_id=message.from_id).first()

    if not user_data.spam:
        await methods.edit_messages(f"{Emoji.NO} Скрипт не включён.")
        return

    await Scripts.filter(user_id=message.from_id).update(spam=False)
    await Spam.filter(user_id=message.from_id, peer_id=message.peer_id).update(is_active=False)

    await methods.edit_messages(f"{Emoji.YES} Спам успешно отключён.")


@spam.message(IsCommand(["-спамы", "-spams"]))
async def delete_all_spams(message: Message):
    methods = APIMethod(message)

    await Spam.filter(user_id=message.from_id).delete()
    await methods.edit_messages(f"{Emoji.YES} Все спамы успешно очищены.")
