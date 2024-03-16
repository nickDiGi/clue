from enum import Enum

'''
Classes used to format messages
'''
class Message:
    def __init__(self, message_type, sender_id, data):
        self.message_type = message_type
        self.sender_id = sender_id
        self.data = data

class Message_Types(Enum):
    CREATE_GAME = 1
    JOIN_GAME = 2
    LOBBY_ROSTER_UPDATE = 3