from config import ProjectData
from pyrogram import Client


class GroupController:
    def __init__(self) -> None:
        self.task = None
        self.bot_token = ProjectData.BOT_TOKEN
        self.session = None

    def init(self):
        self.session = Client(name="telegram_bot", api_id=ProjectData.API_ID,
                                api_hash=ProjectData.API_HASH, bot_token=self.bot_token,
                                workdir='pyrogram_sessions', plugins=dict(root='pyrogram_commands'))
    
    def start(self):
        self.task = self.session.start()

    def stop(self):
        self.task.cancel()

    def restart(self):
        self.stop()
        self.start()
