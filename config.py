import time

tortoise_orm = {
    "connections": {"default": "mysql://***/bot"},
    "apps": {
        "models": {
            "models": ["models.users"],
            "default_connection": "default",
        },
    },
}


class ProjectData:
    START_TIME = int(time.time())

    API_ID = "24589584"
    API_HASH = "775e33cac57785653881f4cec2756bc7"
    BOT_TOKEN = "6642085237:AAGsuZ6g1T_nv-hl2U-qsdy_c_Vg_j_HUdE"

    OWNER_TOKEN = "vk1.a.ulogNOLn21UB_AZ8GuxYsMAtbUFDkzoVhpqVbV_3cRKZCH--cyeCAs4HBmhODxe9p7_bZqgNRaF7VdOdKQKNcsquzio5lODzmFHZslPL84Jq7Cpo4Xl9u-FWTRlkrfEPtG9GwB-2TW6Gh73vRimWJsnMa4Zuk8jPj1JZWDZlQpInPMOsY3UofJTqoJepvB6i1lQv4A5NdAg6jBJEVTUBsA"


class ProjectVariables:
    USERS = {}
    SCRIPTS = {}
    GET_INFO = {
        "default": """
———————————————————
STANDLP 000.1 (ULTIMATE)>Info
———————————————————
🙍‍♂ Nickname> {nickname}
⚠ Spoofer> no
☣ Spam> {spam_status}
🌐 Protection> no
👮‍♂ Staff> {role}
⚙ Asi Scripts> No
🐩 Modder> Yes
⏰ Time> {time}
———————————————————
""",
        "thisby": """
**********
[THISBY MOBULE OFFICE]
__________
[OFFICE-1]
[OFFICE-2]
__________
[PING {ping} sec]
__________
[VERSION - BETA]
[NAME]: {name}
[SURNAME]: {surname}
[NICKNAME]: {nickname}
[STATUS]: {role}
""",
        "reid": """
| 💮 ʀᴇɪᴅ ʙᴏᴛ 💮 |
🍒 ᴄᴛᴀᴛуᴄ: {role}
⛩ʙᴀɯ ᴨᴩᴇɸиᴋᴄ: {prefix}
❓ɪᴅ ʙᴀɯᴇй ᴄᴛᴩᴀницы: {user_id}
📌 ɪᴅ чᴀᴛᴀ: {chat_id}
💬ᴋᴀᴨч ᴩᴇɯᴇно: 0
🩸ᴄᴛᴀᴛуᴄ ᴄᴨᴀʍᴀ: {spam_status}
❤боᴛ ʙ ᴩᴇжиʍᴇ: ᴀᴋᴛиʙный
❗ʙыбᴩᴀн ɯᴀбᴧон ɴ: 1
⚙боᴛ ᴩᴀбоᴛᴀᴇᴛ {worked_time} сек.
""",
        "paradox": """
| Paradox LP |
+Ваш статус: {role}
+Ваш префикс: {prefix}
+ID Чата: {chat_id}
+Статус спама: {spam_status}
+Статус лспама: Выключен
+Бот работает {worked_time} сек.
""",
        "hexvel": """
👑 Информация о пользователе
💰 Баланс пользователя: {balance}
👥 Состав пользователя: Stand
🍀 Никнейм пользователя: {nickname}
⚛ Ранг пользователя: {role}
🔗 Токен пользователя: {is_token}

⚙ Префиксы пользователя:
▶ Префикс команд: {prefix_commands} | .х
▶ Префикс скриптов: {prefix_scripts} | .с
▶ Префикс админа: {prefix_admins} | .а
""",
        "alya": """
⚙ Настройки:

👾 Префикс: {prefix}
💣 Триггер: дд
⏲ Задержка: 3 сек
✏ Редактирование: хы-хы-хы
📢 Редачгс:
👼🏼 Время в раю: {time}

💬 Для настройки используйте [.тук]
""",
    }


class Emoji:
    YES = "✅"
    NO = "❎"
    ERROR = "🚫"
    WARNING = "⚠"
    COMMENT = "💬"
    SETTINGS = "⚙"
    WATCH = "⌚"
    UP = "🔼"
    DOWN = "🔽"
    LEFT = "◀"
    RIGHT = "▶"
    BOY = "♂"
    GIRL = "♀"
    USER = "👤"
    USERS = "👥"
    LOADING = "♻"
    EARTH = "🌐"
    KEY = "🔑"
    HEART = "❤"
    EYE = "👁"
    STATS_UP = "📈"
    STATS_DOWN = "📉"
    I = "🖱"
    MONEY = "💰"
    LINK = "🔗"
    ATTENTION = "❗"
    WAITING = "⏳"
    CLEVER = "🍀"
    KING = "👑"
    SHILD = "🛡"

    ZERO = "0⃣"
    ONE = "1⃣"
    TWO = "2⃣"
    THREE = "3⃣"
    FOUR = "4⃣"
    FIVE = "5⃣"
    SIX = "6⃣"
    SEVEN = "7⃣"
    EIGHT = "8⃣"
    NINE = "9⃣"
    TEN = "🔟"

    B_RED = "🔴"
    B_ORANGE = "🟠"
    B_YELLOW = "🟡"
    B_GREEN = "🟢"
    B_BLUE = "🔵"
    B_PURPLE = "🟣"
    B_BROWN = "🟤"
    B_WHITE = "⚪"
    B_BLACK = "⚫"

    S_RED = "🟥"
    S_ORANGE = "🟧"
    S_YELLOW = "🟨"
    S_GREEN = "🟩"
    S_BLUE = "🟦"
    S_PURPLE = "🟪"
    S_BROWN = "🟫"
    S_WHITE = "⬜"
    S_BLACK = "⬛"

    BOOK_RED = "📕"
    BOOK_GREEN = "📗"
    BOOK_BLUE = "📘"

    PAY_UP = "📤"
    PAY_DOWN = "📥"
    ID = "🆔"
    SI = "⚛"
