import asyncio

from os import getenv

from aiohttp import ClientSession


TG_HOST = getenv('TG_HOST', 'localhost')
BOT_TOKEN = getenv('BOT_TOKEN', 'test')


async def main():
    last_update = None
    params = {}
    while True:
        status, resp = await getUpdates(params=params)
        result = resp['result'][0] # Should get the last one. Not the first. ToDo: Exception handler
        last_update = result['update_id']
        params['offset'] = last_update + 1

        await asyncio.sleep(5)

async def getUpdates(params={}):
    async with ClientSession() as session:
        async with session.get(
            f'{TG_HOST}/{BOT_TOKEN}/getUpdates',
            params=params
        ) as resp:
            return resp.status, await resp.json()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

