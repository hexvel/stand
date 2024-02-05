import asyncio
import loguru

from vkbottle.api import API
from vkbottle.user import User, UserLabeler
from vkbottle import BuiltinStateDispenser, CaptchaError

from config import ProjectVariables
from models import Scripts, Users
from user import user_labelers
from user.script_controller import ScriptController


class DataUser:
    OWNER_ID: int

    def __init__(self, user: Users):
        self.prefix_commands = [".х", user.prefix_commands]
        self.scripts_prefix = [".с", user.prefix_scripts]
        self.admin_prefix = [".а", user.prefix_admin]
        self.ignore_list = [user.ignore_list]
        self.trust_prefix = [user.trust_prefix]
        self.trust_list = [user.trust_list]


class UserController:
    def __init__(self, user: Users, script_model: Scripts) -> None:
        self.task = None
        self.session = None
        self.user = user
        self.data = DataUser(self.user)

        self.script_model = script_model

    async def init(self):
        api = API(token=self.user.token)
        user = UserLabeler()

        await api.account.get_info()

        for labeler in user_labelers:
            user.load(labeler)

        self.session = User(
            api=api, labeler=user, state_dispenser=BuiltinStateDispenser()
        )

        ProjectVariables.SCRIPTS[self.user.user_id] = ScriptController(
            api, self.script_model
        )
        
        await ProjectVariables.SCRIPTS[self.user.user_id].run_script_listener()

    def start(self):
        self.task = asyncio.create_task(self.session.run_polling())

    def stop(self):
        self.task.cancel()

    def restart(self):
        self.stop()
        self.start()

    async def run(self) -> bool:
        try:
            await self.init()
        except:
            return False
        else:
            self.start()
            return True
