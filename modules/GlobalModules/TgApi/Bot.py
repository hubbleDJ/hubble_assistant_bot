"""API для работы с телеграм ботом"""

import asyncio
import aiohttp
import json

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
        updates = Update(response)
        
        if updates.update_id + 1 > self.update_id:
            self.update_id = updates.update_id + 1
        
        return updates

    def send_message(self, chat_id: int, text: str, buttons: list=[], drop_buttons: bool=True, reply_to_message_id: int = None) -> None:
        """Отправка сообщения"""
        
        if text not in [None, '']:
            payload = {
                "chat_id": str(chat_id),
                "text": text[:4095]
            }

            if reply_to_message_id: payload['reply_to_message_id'] = reply_to_message_id
                
            if buttons and len(buttons) > 0:
                payload["reply_markup"] = {
                    "keyboard": [[{"text": text}] for text in buttons],
                    "remove_keyboard": True,
                    "resize_keyboard": True,
                    "one_time_keyboard": False
                }
            else:
                payload["reply_markup"] = {
                    "remove_keyboard": drop_buttons
                }

            asyncio.run(
                self.AcyncRequest(
                    url=f'{self.tg_url}/sendMessage',
                    params=payload,
                    is_json=True
                )
            )
        
    @staticmethod
    async def AcyncRequest(url: str, params: dict={}, request_type: str='get', is_json: bool=False):
        '''Запросы http/https'''
        
        async with aiohttp.ClientSession() as session:
            if request_type == 'post' and not is_json:
                async with session.post(url, params=params) as resp:
                    return await resp.json()
            elif request_type == 'get' and not is_json:
                async with session.get(url, params=params) as resp:
                    return await resp.json()
            elif request_type == 'post' and is_json:
                async with session.post(url, json=params) as resp:
                    return await resp.json()
            elif request_type == 'get' and is_json:
                async with session.get(url, json=params) as resp:
                    return await resp.json()
            
                

if __name__ == '__main__':
    from Update import Update
    bot = Bot(token='8082634489:AAFNYVOZXWme-aHWulTOMneZ5Hudr5mEg4A')
    print(bot.GetUpdates())