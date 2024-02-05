import loguru
from vkbottle.user import Message, UserLabeler

from config import Emoji
from functions.base_functions import search_user_id
from models.users import Pattern, Users
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixCommand
from rules.from_me import IsFromMe
from utils import APIMethod

patterns = UserLabeler()
patterns.auto_rules = [IsFromMe(), IsPrefixCommand()]


def delete_elements(text: str, elements: list):
    for del_element in elements:
        text = str(text).replace(f"{del_element}", "")
    return text


@patterns.message(IsCommand(["+шаб", "+pat"]))
async def pattern_add(message: Message):
    methods = APIMethod(message)

    response = await message.ctx_api.messages.get_by_id(
        message_ids=message.id, extended=1
    )

    data_type: list = []
    data_attachment: list = []

    try:
        data_name = message.text.split("\n")[0].split(" ")[2]
    except:
        data_name = None

    if await Pattern.filter(user_id=message.from_id, name=data_name):
        await methods.edit_messages(
            f"{Emoji.WARNING} Шаблон с таким названием уже существует."
        )

    if response.items[0].reply_message:
        data_message = response.items[0].reply_message
    else:
        data_message = response.items[0]

    if "out" in data_message:
        try:
            data_text = message.text.split("\n")[1]
        except:
            data_text = None
    else:
        if data_message.text:
            data_text = data_message.text
        else:
            data_text = "None"

    if data_text:
        data_type.append("text")

    if not data_message.attachments:
        data_attachment = None

    if data_attachment is None and data_text is None:
        send_message = f"{Emoji.WARNING} Нет элементов для создания шаблона."
        await methods.edit_messages(send_message)
        return

    for data_pool in enumerate(data_message.attachments):
        data_int = data_pool[0]
        data = data_pool[1]
        _type = data_message.attachments[data_int].type._value_

        if data.photo:
            data = data.photo
        elif data.doc:
            data = data.doc
        elif data.video:
            data = data.video
        elif data.audio_message:
            data = data.audio_message
        elif data.link:
            data = data.link
        elif data.audio:
            data = data.audio
        elif data.graffiti:
            data = data.graffiti

        if data.access_key:
            access_key = data.access_key
        else:
            access_key = False
        owner_id = data.owner_id

        if access_key:
            attachment = f"{_type}{owner_id}_{data.id}_{access_key}"
        else:
            attachment = f"{_type}{owner_id}_{data.id}"

        data_type.append(_type)
        data_attachment.append(attachment)
        if data_name is None:
            send_message = f"{Emoji.WARNING} Необходимо указать название."
            await methods.edit_messages(send_message)
            return

    attachment = delete_elements(text=data_attachment, elements=["[", "]", " ", "'"])
    types = delete_elements(text=data_type, elements=["[", "]", " ", "'"])

    await Pattern.create(
        user_id=message.from_id,
        name=data_name,
        attachments=attachment,
        text=data_text,
        types=types,
    )

    send_message = f"{Emoji.YES} Шаблон ['{data_name}'] успешно создан\n{Emoji.HEART} Типы вложений: [' {types} ']."
    await methods.edit_messages(send_message)


@patterns.message(IsCommand(["шаб", "pat"]))
async def get_pattern(message: Message):
    methods = APIMethod(message)

    if len(message.text.split()) < 3:
        await methods.edit_messages(f"{Emoji.NO} Не указано название шаблона.")
        return

    name = message.text.split()[2]
    get_db = await Pattern.filter(user_id=message.from_id, name=name).first()

    if get_db is None:
        await methods.edit_messages("❎ Нет шаблона с таким именем.")
        return

    text = None if get_db.text == "None" else get_db.text
    attachments = None if get_db.attachments == "None" else get_db.attachments
    await methods.edit_messages(text=text, attachments=attachments)


@patterns.message(IsCommand(["шабы", "pats"]))
async def pattern_add(message: Message):
    methods = APIMethod(message)
    send_message = f"{Emoji.YES} Список ваших шаблонов:\n\n"
    get_db = await Pattern.filter(user_id=message.from_id)
    if get_db is None:
        await methods.edit_messages(f"{Emoji.NO} Ни одного шаблона.")
        return
    for count, pat in enumerate(get_db, 1):
        send_message += "{count}. -> [' {name} '] | -> {type}\n".format(
            count=count, name=pat.name, type=pat.types
        )
    send_message += f"\n{Emoji.COMMENT} Чтобы вызвать шаблон введите команду [prefix] шаб [название]"
    await methods.edit_messages(send_message)


@patterns.message(IsCommand(["-шаб", "-pat"]))
async def pattern_add(message: Message):
    methods = APIMethod(message)
    if len(message.text.split()) >= 3:
        name = message.text.split()[2]
        if await Pattern.filter(user_id=message.from_id, name=name).first():
            await Pattern.filter(user_id=message.from_id, name=name).delete()
            await methods.edit_messages(f"{Emoji.YES} Шаблон удален.")
            return
        await methods.edit_messages(f"{Emoji.NO} Шаблон не найден.")
