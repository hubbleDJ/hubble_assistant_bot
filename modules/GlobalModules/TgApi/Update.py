from .Message import Message

class Update:
    def __init__(self, update_response: dict, update_id: int=0):
        
        self.update_id = update_id
        self.messages: str = []
        self.cahannel_posts = []
        self.update_types = {}
        
        if 'ok' in update_response and update_response['ok'] and 'result' in update_response:
            print(update_response)