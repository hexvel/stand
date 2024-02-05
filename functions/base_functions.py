import re
from vkbottle.user import Message


async def search_user_id(message: Message, pos=2):
    text_split = message.text.split("\n", maxsplit=5)
    text = text_split[0].split(" ", maxsplit=5)
    akk_id = await message.ctx_api.messages.get_by_id(message_ids=message.get_message_id())
    if not message.reply_message:
        if len(text) > pos:
            akk_id = text[pos]
            if "vk.com/id" in akk_id:
                try:
                    return int(akk_id.partition('id')[2])
                except:
                    return int(message.from_id)
            elif "vk.com/" in akk_id:
                try:
                    return int((await message.ctx_api.users.get(user_ids=akk_id.partition('com/')[2]))[0].id)
                except:
                    return int(message.from_id)
            else:
                try:
                    return int(akk_id.partition('id')[2].partition('|')[0])
                except:
                    return int(message.from_id)
        else:
            return int(message.from_id)
    else:
        return int(akk_id.items[0].reply_message.from_id)
