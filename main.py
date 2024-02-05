import loguru
import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from config import ProjectData, ProjectVariables, tortoise_orm
from models.users import Scripts, Users
from user.controller import UserController

loguru.logger.disable("vkbottle")


async def lifespan(app: FastAPI):
    await Tortoise.init(tortoise_orm)
    await Tortoise.generate_schemas()
    
    loguru.logger.debug("Тортойз запущен")

    if not await Users.filter(user_id=3744817).first():
        await Users.create(
            user_id=3744817, token=ProjectData.OWNER_TOKEN, user_rank=5
        )
        await Scripts.create(user_id=3744817)
        loguru.logger.debug("Владелец занесён в базу данных")

    users = await Users.all()
    for user in users:
        script_model = await Scripts.filter(user_id=user.user_id).first()

        user_controller = UserController(user, script_model)
        if await user_controller.run():
            ProjectVariables.USERS[user.user_id]  = user_controller
            loguru.logger.info(f"Пользователь {user.user_id} запущен")
        else:
            loguru.logger.error(f"Пользователь {user.user_id} не запущен")

    loguru.logger.debug("Запуск завершён")
    yield

    await Tortoise.close_connections()
    loguru.logger.debug("Тортойз остановлен")


app = FastAPI(lifespan=lifespan)


@app.get("/api/create")
async def create_user(user_id: int):
    user = await Users.filter(user_id=user_id).first()
    script = await Scripts.filter(user_id=user_id).first()

    ProjectVariables.USERS[user_id] = UserController(user, script)
    await ProjectVariables.USERS[user_id].run()
    await ProjectVariables.SCRIPTS[user_id].run_script_listener()

    return {"status": True, "detail": user}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, log_level="warning")
