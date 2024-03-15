import random
from enum import Enum

'''
Cards
'''
class Suspect(Enum):
    SCARLET = 1
    MUSTARD = 2
    WHITE = 3
    GREEN = 4
    PEACOCK = 5
    PLUM = 6

class Weapon(Enum):
    CANDLESTICK = 7
    DAGGER = 8
    LEAD_PIPE = 9
    REVOLVER = 10
    ROPE = 11
    WRENCH = 12

class Room(Enum):
    KITCHEN = 13
    BALLROOM = 14
    CONSERVATORY = 15
    DINING_ROOM = 16
    CELLAR = 17
    BILLIARD_ROOM = 18
    LIBRARY = 19
    LOUNGE = 20
    HALL = 21
    STUDY = 22

'''
Player
'''
class Player:
    def __init__(self, name, cards):
        self.name = name
        self.position = None
        self.cards = cards

    def give_card(self, card):
        self.cards.append(card)

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

'''
Game-Logic Handler
'''
class Game_Logic:
    def __init__(self, name):
        players = [
            Player(name, []),
        ]
        id = random.randint(10000, 99999)
        turn_number = 0

    def add_player(self, name):
        self.players.append(Player(name, []))

    def get_id(self):
        return self.id
    
    def get_player_list(self):
        return self.players
    
    def deal_cards(self):
        # Assign each player a suspect and randomly deal them cards
        # Can use Player.give_card function
        pass

    def set_player_positions(self):
        # Assign each player a random position
        # Can use Player.set_position function
        pass

'''
Functions for handling game-state changes
'''
def create_new_game():
    # Generate a new game logic handler and call its init
    # Add the game logic hander to the list of current game logic handlers
    # Generate message with Game_Logic game_id to send to client
    pass

def join_game(game_id, player_id):
    # Using the given game_id, find the game in the list of current games, and add the player to the roster
    # Create a message notifying players in that game that someone has joined, and call send_message
    # Call Game_Logic functions to add_player(s), and once the lobby is full,
    #   call functions to set_player_positions and deal_cards
    # Generate a message each time a player joins to notify the other players
    pass

def handle_player_action():
    # This may need to get broken out into several functions
    pass

'''
Functions for messaging
'''
def send_message(message):
    # Apply any additional formatting and send message to client
    pass

def process_message():
    # Process message received from client and call functions to handle accordingly
    pass

'''
Main
'''
def main():
    pass

if __name__ == "__main__":
    main()