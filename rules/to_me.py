from vkbottle import ABCRule
from vkbottle.user import Message
from loguru import logger as l


class NotFromMe(ABCRule):
    async def check(self, message: Message):
        if message.out != 1:
            return {"user_id": message.from_id}
        return False
