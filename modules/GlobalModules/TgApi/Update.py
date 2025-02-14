from .Message import Message

class Update:
    def __init__(self, update_response: dict, update_id: int=0):
        
        self.update_id = update_id
        self.messages: list[Message] = []
        self.cahannel_posts: list = []
        
        print(update_response)
        
        if 'ok' in update_response and update_response['ok'] and 'result' in update_response:
            for result in sorted(update_response['result'], key=lambda result: result['update_id']):
                if 'update_id' in result and result['update_id'] > self.update_id:
                    self.update_id = result['update_id']
                if 'message' in result:
                    self.messages.append(Message(result['message']))
