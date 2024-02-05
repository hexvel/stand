from vkbottle.user import Message, UserLabeler

from config import Emoji
from models.users import Scripts
from rules.check_command import IsCommand
from rules.check_prefix import IsPrefixScript
from rules.from_me import IsFromMe
from utils import APIMethod

cover = UserLabeler()
cover.vbml_ignore_case = True
cover.auto_rules = [IsPrefixScript(), IsFromMe()]


@cover.message(IsCommand(["обложка", "cover"]))
async def change_cover_script_wrapper(message: Message):
    methods = APIMethod(message)
    message_split = message.text.split(maxsplit=2)

    if len(message_split) <= 2:
        await methods.edit_messages(f"{Emoji.WARNING} Укажите тему обложки.")
        return

    update_theme = message_split[2]
    if update_theme.isdigit():
        await Scripts.filter(user_id=message.from_id).update(cover_id=update_theme)
        await methods.edit_messages(
            f"{Emoji.YES} Тема обложки обновлена на ['{update_theme}']."
        )
    else:
        await methods.edit_messages(f"{Emoji.NO} Укажите тему в виде индексации.")


@cover.message(IsCommand(["автообл", "autocover"]))
async def change_autocover_script_wrapper(message: Message):
    methods = APIMethod(message)

    user_data = await Scripts.filter(user_id=message.from_id).first()

    if user_data.auto_cover:
        await Scripts.filter(user_id=message.from_id).update(auto_cover=False)
        await methods.edit_messages(f"{Emoji.YES} Скрипт автообложек выключен.")
        return

    await Scripts.filter(user_id=message.from_id).update(auto_cover=True)
    await methods.edit_messages(f"{Emoji.YES} Скрипт автообложек включён.")
