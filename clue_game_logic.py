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
    def __init__(self, name, address, cards):
        self.name = name
        self.address = address
        self.position = None
        self.cards = cards

    def get_name(self):
        return self.name

    def give_card(self, card):
        self.cards.append(card)

    def get_address(self):
        return self.address

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

'''
Game-Logic Handler
'''
class Game_Session:
    def __init__(self, name, address):
        self.players = [
            Player(name, address, []),
        ]
        self.id = random.randint(10000, 99999)
        self.turn_number = 0

    def add_player(self, name, address):
        self.players.append(Player(name, address, []))

    def get_players(self):
        return self.players

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