import asyncio
import traceback

from telethon import TelegramClient
from telethon.errors import UsernameOccupiedError, UsernameInvalidError
from telethon.events import NewMessage
from telethon.tl.functions.channels import UpdateUsernameRequest
from telethon.tl.types import PeerChannel

SESSION_NAME = 'SetChannelLink'
API_ID = 1209411
API_HASH = '32583db8454ca7feb52a4a5d48289519'

DELAY = 30
LINKS_POOL = ['anime', 'hentai', 'anime_ru']

CHANNEL_ID = 123456  # ID канала юзернейм которого хотим поменять. Без -100 в начале!


def main():
    # async def process():
    #     channel = await client.get_entity(PeerChannel(CHANNEL_ID))
    #
    #     while True:
    #         link = await try_to_set_username(channel)
    #
    #         if link:
    #             print(f'Username "{link}" is available!')
    #             break
    #
    #         await asyncio.sleep(DELAY)
    #
    # async def try_to_set_username(channel):
    #     for link in LINKS_POOL:
    #         try:
    #             await client(UpdateUsernameRequest(channel, link))
    #             return link
    #
    #         # Юзернейм уже занят:
    #         except UsernameOccupiedError:
    #             print('Occupied!')
    #             pass
    #
    #         # Юзернейм не занят, но и не доступен:
    #         except UsernameInvalidError:
    #             print('Invalid!')
    #             pass
    #
    #         # Другая ошибка:
    #         except Exception:
    #             print(traceback.format_exc())
    #
    #         finally:
    #             await asyncio.sleep(2)

    loop = asyncio.get_event_loop()
    client = TelegramClient(
        session=SESSION_NAME,
        api_id=API_ID,
        api_hash=API_HASH,
        loop=loop
    )

    client.start()

    @client.on(NewMessage(pattern='Привет'))
    async def hello_func(event: NewMessage.Event):
        print('Hello world')

    client.run_until_disconnected()

# loop.run_until_complete(process())


if __name__ == '__main__':
    main()