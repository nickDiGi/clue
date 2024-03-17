from enum import Enum

'''
Classes used to format messages
'''
# Note: game_state_data represents high level game info such as players positions on the board
#       while player_state_data represents data about the individual player such as their cards
class Message:
    def __init__(self, message_type, sender_id, game_state_data, player_state_data):
        self.message_type = message_type
        self.sender_id = sender_id
        self.game_state_data = game_state_data
        self.player_state_data = player_state_data

class Message_Types(Enum):
    CREATE_GAME = 1
    JOIN_GAME = 2
    LOBBY_ROSTER_UPDATE = 3
    GAME_STATE_UPDATE = 4
    YOUR_TURN_NOTIFICATION = 5