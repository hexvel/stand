import asyncio
import requests
import random
import time

from vk_api import VkApi
from datetime import datetime
import vk_captchasolver as vc
from loguru import logger

from vkbottle import API
from lib.cover import CoverImage
from models import Scripts, Spam, Users


class ScriptController:
    def __init__(self, api: API, model: Scripts):
        self.api = api
        self.model = model

        self.__task = None
        self.token = None
        self.vk_api = None
        self.spam_model = self.model.spam
        self.auto_online = self.model.auto_online
        self.auto_offline = self.model.auto_offline
        self.auto_sms = self.model.auto_sms

        self.auto_cover = self.model.auto_cover
        self.start_condition_cover = 0
        self.stop_condition_cover = 0

    def captcha_handler(self, captcha):
        captcha.get_image()
        url = captcha.get_url()

        r = requests.get(url, stream=True)
        with open("captcha.png", "wb") as out:
            out.write(r.content)

        try:
            random_time_sleep_captcha_main = random.randrange(3, 4)
            time.sleep(int(random_time_sleep_captcha_main))

            return captcha.try_again(vc.solve(image='captcha.png'))
        except:
            random_time_sleep_captcha = random.randrange(3, 4)
            time.sleep(int(random_time_sleep_captcha))
            try:
                return captcha.try_again(vc.solve(image='captcha.png'))
            except:
                random_time_sleep_captcha2 = random.randrange(5, 6)
                time.sleep(int(random_time_sleep_captcha2))
                return captcha.try_again(vc.solve(image='captcha.png'))

    async def auto_cover_recovery(self):
        data = await Scripts.filter(user_id=self.model.user_id).first()
        cover = CoverImage(self.api, data.user_id, data.cover_id)

        try:
            cover.draw()
            await cover.upload()
        except:
            logger.warning(f"У пользователя {self.model.user_id} не обновилась обложка.")

        start = time.time()
        stop = random.randint(60, 70)

        return start, stop

    async def spam_function(self) -> None:
        data = await Spam.filter(user_id=self.model.user_id).all()

        if not data: return

        with open("templates/shablon_reply.txt", "r", encoding="utf-8") as file:
            template = file.readlines()
            template_text = random.choice(template)[:-1]

        for peer in data:
            if not peer.is_active:
                continue

            self.vk_api.messages.send(
                peer_id=peer.peer_id,
                message=peer.text.replace("'ez'", template_text),
                attachment=peer.attachments,
                random_id=0
            )
            await asyncio.sleep(peer.spam_sleep)

    async def check_script_status(self) -> bool:
        data = await Scripts.filter(user_id=self.model.user_id).first()
        spam_data = await Spam.filter(user_id=self.model.user_id).first()
        user_data = await Users.filter(user_id=self.model.user_id).first()

        self.spam_model = True if spam_data else False
        self.auto_online = data.auto_online
        self.auto_offline = data.auto_offline
        self.auto_sms = data.auto_sms
        self.auto_cover = data.auto_cover
        self.token = user_data.token
        self.vk_api = VkApi(token=self.token, captcha_handler=self.captcha_handler).get_api()

        return True

    async def listen_to_events(self):
        while True:
            scripts_status = await self.check_script_status()
            if not scripts_status:
                await asyncio.sleep(10)

            if self.spam_model:
                await asyncio.create_task(self.spam_function())

            if self.auto_cover:
                if (
                        self.start_condition_cover + self.stop_condition_cover
                ) < time.time():
                    start, stop = await self.auto_cover_recovery()
                    self.start_condition_cover = start
                    self.stop_condition_cover = stop

    async def run_script_listener(self) -> None:
        loop = asyncio.get_event_loop()
        self.__task = loop.create_task(self.listen_to_events())

    async def stop_script_listener(self) -> None:
        logger.success("Stopping script listener")
        self.__task.cancel()

    async def restart_scripts(self) -> None:
        await self.stop_script_listener()
        await self.run_script_listener()
