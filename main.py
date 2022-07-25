import asyncio
from typing import Tuple

from dotenv import load_dotenv
from os import getenv

from aiohttp import ClientSession


# ToDo
# Parse user messages
# Use commands (set kindle email)
# Set user data in local storage


class STATUSES:
    SUCCESS = 200
    CREATED = 201


class BotAPI:
    class URI:
        GET_UPDATES = 'getUpdates'
        SET_COMMANDS = 'setMyCommands'

    def __init__(self, host, token) -> None:
        self.base_url = f'{host}/{token}/'
        self.commands = {}
        self.user_storage  = {}

    def isCommand(self, data: dict) -> bool:
        return 'entities' in data

    async def initBaseCommands(self) -> None:
        base_commands = (
            {
                'command': 'setKindle',
                'description': 'Send me your Kindle email address'
            },
        ) 
        status = await self.setMyCommands(base_commands)
        if status == STATUSES.SUCCESS:
            self.commands.update({k: v for k, v in base_commands})


    async def getUpdates(self, params=None) -> Tuple[int, dict]:
        async with ClientSession() as session:
            async with session.get(
                self.base_url + self.URI.GET_UPDATES,
                params=params
            ) as resp:
                return resp.status, await resp.json()

    async def setMyCommands(
        self,
        commands: tuple[dict],
        scope=None,
        language_code: str= None) -> int:
        async with ClientSession() as session:
            async with session.post(
                self.base_url + self.URI.SET_COMMANDS,
                json={'commands': commands}
            ) as resp:
                return resp.status


async def main():
    TG_HOST = getenv('TG_HOST', 'localhost')
    BOT_TOKEN = getenv('BOT_TOKEN', 'test')

    bot = BotAPI(TG_HOST, BOT_TOKEN)
    last_update = None
    params = {}
    while True:
        print('Prepare to get updates')
        status, resp = await bot.getUpdates(params=params)
        print(status, resp)
        results = resp['result']
        if status == STATUSES.SUCCESS and results:
            last_update = results[-1]['update_id']
            result = results[0] # ToDo: Exception handler
            params['offset'] = last_update + 1

        await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        load_dotenv()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

