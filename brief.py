import re
import sys
from datetime import datetime, timedelta

from telethon import TelegramClient
from telethon.events import NewMessage

from config import config
from resources.models import loop
from resources.tools import bot_logging
from src.content import BRIEF_ALLIANCE_PARSE


def main():
    client = TelegramClient(config.BRIEF_SESSION_NAME, config.API_ID, config.API_HASH, loop=loop)
    channels = [config.MY_TESTING_CHANNEL, config.CHAT_WARS_DIGEST]

    # '🤝Headquarters news:'
    @client.on(
        NewMessage(func=lambda c: '123' in c.message.message and c.message.to_id.channel_id in channels)
    )
    async def brief_headquarters(event: NewMessage.Event):
        message = event.message

        if message.fwd_from is None:
            date = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            message_id = message.id

        else:
            date = str(message.fwd_from.date + timedelta(hours=3))[:-6]
            message_id = message.fwd_from.channel_post

        answer = '<i>🤝Альянсы:</i>\n'

        for hq in message.message.replace('🤝Headquarters news:\n', '').split('\n\n\n'):
            pass

    async def hq_parsing(hq: str):
        parse = re.search(BRIEF_ALLIANCE_PARSE, hq)

        hq_name = parse.group('head_name')

    client.start()
    client.run_until_disconnected()


if __name__ == '__main__':
    # Process Name (for Linux)
    if sys.platform == 'linux':
        import ctypes

        libc = ctypes.cdll.LoadLibrary('libc.so.6')
        libc.prctl(15, 'B', 0, 0, 0)

    # Set Logging
    bot_logging.set_logging(config.debug, 'logs/brief.log')

    main()
