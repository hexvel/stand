import random
from random import choice

import loguru
from vkbottle.user import Message, UserLabeler

from models.users import Scripts, Users
from rules.to_me import NotFromMe
from user.data import UserData

handlers = UserLabeler()
handlers.auto_rules = [NotFromMe()]


@handlers.message()
async def listen(message: Message):
    user_info = await message.ctx_api.account.get_profile_info()
    get_db = await Users.filter(user_id=user_info.id).first()

    if message.from_id in get_db.trust_list:
        if message.text.split(" ")[0] == get_db.trust_prefix:
            await message.ctx_api.messages.send(
                peer_id=message.peer_id,
                message=message.text.split(" ", 1)[1],
                random_id=0,
            )

    if message.from_id in get_db.troll_list:
        with open("templates/shablon_reply.txt", "r", encoding="utf-8") as file:
            lines = [line for line in file]
            send_message = "[id{}|👽] {}".format(message.from_id, choice(lines))
        await message.ctx_api.messages.send(
            peer_id=message.peer_id, message=send_message, random_id=0
        )

    if message.from_id in get_db.ignore_list:
        await message.ctx_api.request(
            "messages.delete",
            {
                "peer_id": message.peer_id,
                "cmids": message.conversation_message_id,
                "delete_for_all": 0,
            },
        )

    scripts = await Scripts.filter(user_id=user_info.id).first()
    if (
            scripts.auto_sms
            and message.peer_id not in scripts.auto_sms_users['users']
            and message.from_id in scripts.auto_sms_users['users']
    ):
        with open("templates/shablon_reply.txt", "r", encoding="utf-8") as file:
            template = file.readlines()
            template_text = random.choice(template)[:-1]

        await message.reply(
            scripts.auto_sms_text.replace("'ez'", template_text).replace(
                "None", template_text
            )
        )
