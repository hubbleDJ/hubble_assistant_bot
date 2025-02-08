
import aiohttp
import asyncio

async def async_request(url: str, params: dict={}, request_type: str='get'):
    async with aiohttp.ClientSession() as session:
        if request_type == 'post':
            async with session.post(url, params=params) as resp:
                return await resp.json()
        else:
            async with session.get(url, params=params) as resp:
                return await resp.json()

t = 1

if __name__ == '__main__':
    print(asyncio.run(async_request(
        url='https://api.telegram.org/bot8082634489:AAFNYVOZXWme-aHWulTOMneZ5Hudr5mEg4A/getUpdates',
        request_type='post'
    )))