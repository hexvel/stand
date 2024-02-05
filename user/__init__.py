from .command.admin_commands import admin_command
from .command.chat_commands import chat_commands
from .command.default_commands import default_commands
from .command.handlers import handlers
from .command.list_commands import list_commands
from .command.pattern_commands import patterns
from .scripts.add_spam import spam
from .scripts.autosms import autosms_scripts
from .scripts.auto_cover import cover

user_labelers = [
    spam,
    cover,
    autosms_scripts,
    handlers,
    admin_command,
    chat_commands,
    default_commands,
    list_commands,
    patterns,
]
