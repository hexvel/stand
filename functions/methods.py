from loguru import logger as log


async def edit_messages(message, text = None, attachments = None):
    try: await message.ctx_api.messages.edit(peer_id=message.peer_id, message=text, attachment=attachments, message_id=message.id)
    except Exception as e: log.error(e)

async def send_messages(message, text = None, attachments = None):
    try: await message.ctx_api.messages.send(peer_id=message.peer_id, message=text, attachment=attachments, random_id=0)
    except Exception as e: log.error(e)