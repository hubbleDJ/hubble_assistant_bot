"""API для работы с телеграм ботом"""

import asyncio
import aiohttp

if __name__ == '__main__':
    from Update import Update
else:
    from .Update import Update

class Bot:
    def __init__(self, token: str):
        self.token = token
        self.update_id = 0
        self.tg_url = f'https://api.telegram.org/bot{self.token}'
        
        self.get_me()
    
    def get_me(self) -> None:
        '''Получает информацию о боте'''
        
        response = asyncio.run(self.AcyncRequest(
            url=f'{self.tg_url}/getMe',
            request_type='get'
        ))
        
        if (
            'ok' in response and response['ok'] and
            'result' in response and len(response['result']
        ) > 0):
            for key, value in response['result'].items():
                setattr(self, key, value)
        
        
    def get_updates(self) -> Update:
        '''Получение обновлений из бота'''
        
        response = asyncio.run(
            self.AcyncRequest(
                url=f'{self.tg_url}/getUpdates',
                params={'offset': self.update_id}
            )
        )
        
        return Update(response)
    
    def set_message(self) -> None:
        pass

    @staticmethod
    async def AcyncRequest(url: str, params: dict={}, request_type: str='get'):
        '''Запросы http/https'''
        
        async with aiohttp.ClientSession() as session:
            if request_type == 'post':
                async with session.post(url, params=params) as resp:
                    return await resp.json()
            else:
                async with session.get(url, params=params) as resp:
                    return await resp.json()
                

if __name__ == '__main__':
    from Update import Update
    bot = Bot(token='8082634489:AAFNYVOZXWme-aHWulTOMneZ5Hudr5mEg4A')
    print(bot.GetUpdates())