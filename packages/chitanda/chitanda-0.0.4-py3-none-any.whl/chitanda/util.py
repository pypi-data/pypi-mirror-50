import logging
import re
import sys

from chitanda import CONFIG_DIR, DATA_DIR
from chitanda.config import config
from chitanda.errors import NoCommandFound

logger = logging.getLogger(__name__)


class Message:
    def __init__(self, bot, listener, target, author, contents, private):
        self.bot = bot
        self.listener = listener
        self.target = target
        self.author = author
        self.contents = contents
        self.private = private

    def call_command(self):
        if self.contents.startswith(config['trigger_character']):
            self.contents = self.contents[1:]
            for trigger, command in self._get_sorted_commands():
                if self.contents == trigger or self.contents.startswith(
                    f'{trigger} '
                ):
                    self.contents = self.contents[len(trigger) + 1 :]
                    logger.info(f'Command triggered: {trigger}.')
                    return command.call(self)

        raise NoCommandFound

    def _get_sorted_commands(self):
        modules = set(
            config['modules'].get('global', [])
            + config['modules'].get(str(self.listener), [])
        )
        commands = {
            k: v
            for k, v in self.bot.commands.items()
            if get_module_name(v.__name__) in modules
        }
        return sorted(commands.items(), key=lambda t: len(t[0]), reverse=True)


def get_module_name(full_name):
    return full_name.replace('chitanda.modules.', '', 1).split('.')[0]


def create_app_dirs():
    logger.debug('Creating config and data directories if nonexistent.')
    try:
        CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        DATA_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    except PermissionError:
        logger.critical(
            f'Could not create either config directory ({CONFIG_DIR}) '
            f'or data directory ({DATA_DIR}).'
        )
        sys.exit(1)


def irc_unstyle(text):
    """
    Taken from Makoto Fujimoto's ircmessage library.

    The MIT License (MIT)
    Copyright (c) 2015 Makoto Fujimoto
    """
    for code in ['\x0F', '\x02', '\x1D', '\x1F']:
        text = text.replace(code, '')
    return re.sub(r'\x03(?P<fg>\d{2})(,(?P<bg>\d{2}))?', '', text)


def trim_message(message, length=240):
    if len(message) > length:
        return f'{message[:length - 3]}...'
    return message
