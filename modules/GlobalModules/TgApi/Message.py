"""Сообщения"""

from .Document import Document
from .Photo import Photo
from .Voice import Voice

class Message:
    """"""
    
    def __init__(self, message: dict, previous_message=None):
        
        self.documents: list = [] # type: ignore
        self.photos: list = [] # type: ignore
        self.voices: list = [] # type: ignore
        
        self.message_id = message.get('message_id')
        self.text = message.get('text')
        self.datetime = message.get('date')
        self.message_thread_id = message.get('message_thread_id')
        self.is_forum = message.get('is_forum')
        
        if 'from' in message:
            self.user_id = message['from'].get('id')
            self.message_from_bot = message['from'].get('is_bot')
            self.user_first_name = message['from'].get('first_name')
            self.user_username = message['from'].get('username')
            self.user_language_code = message['from'].get('language_code')
            self.user_is_premium = message['from'].get('is_premium')
            
        if 'chat' in message:
            self.chat_id = message['chat'].get('id')
            self.chat_first_name = message['chat'].get('first_name')
            self.chat_username = message['chat'].get('username')
            self.chat_type = message['chat'].get('type')
        
        if 'document' in message:
            self.documents.append(Document(message['document']))
    
        if 'photo' in message:
            self.photos.append(Photo(message['photo']))
        
        if 'voice' in message:
            self.voices.append(Voice(message['voice']))
