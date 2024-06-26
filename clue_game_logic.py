import random
from enum import Enum

# Constants
HALLWAY_LIMIT = 22

'''
Cards
'''
class Suspect(Enum):
    GREEN = 1
    WHITE = 2
    PEACOCK = 3
    PLUM = 4
    SCARLET = 5
    MUSTARD = 6

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
    BILLIARD_ROOM = 17
    LIBRARY = 18
    LOUNGE = 19
    HALL = 20
    STUDY = 21
    HALLWAY_CONS_BALR = 22
    HALLWAY_BALR_KITC = 23
    HALLWAY_CONS_LIBR = 24
    HALLWAY_LIBR_STDY = 25
    HALLWAY_HALL_LOUG = 26
    HALLWAY_DINR_LOUG = 27
    HALLWAY_BALR_BILR = 28
    HALLWAY_KITC_DINR = 29
    HALLWAY_LIBR_BILR = 30
    HALLWAY_BILR_DINR = 31
    HALLWAY_BILR_HALL = 32
    HALLWAY_STDY_HALL = 33

def match_suspect(string):
    for suspect in Suspect:
        if string == suspect.name:
            return suspect
    return None

'''
Player
'''
class Player:
    def __init__(self, name, address, character):
        self.name = name
        self.address = address
        self.character = match_suspect(character)
        self.cards = []
        self.turn_order_number = None
        self.position = None
        self.lost_game = False

    def get_name(self):
        return self.name
    
    def get_address(self):
        return self.address

    def give_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def set_turn_order_number(self, turn_order_number):
        self.turn_order_number = turn_order_number

    def get_turn_order_number(self):
        return self.turn_order_number

    def set_character(self, character):
        self.character = character

    def get_character(self):
        return self.character

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position
    
    def set_lost_game(self, lost_game):
        self.lost_game = lost_game

    def get_lost_game(self):
        return self.lost_game
    
    def __str__(self):
        return f"Player(name='{self.name}', turn_order_number={self.turn_order_number}, character='{self.character}', position='{self.position}, cards={self.cards}')"

'''
Game-Logic Handler
'''
class Game_Session:
    def __init__(self, name, address, character):
        self.players = [
            Player(name, address, character),
        ]
        # TODO: Check below random number to ensure that it does not match the ID of an existing game
        self.id = random.randint(10000, 99999)
        self.turn_number = 1
        self.suggestion_turn_number = 1
        self.active_suggestion_cards = []
        self.suggesting_player = None
        self.winning_cards = []

    def add_player(self, name, address, character):
        self.players.append(Player(name, address, character))

    def get_players(self):
        return self.players

    def get_id(self):
        return self.id
    
    def get_player_list(self):
        return self.players
    
    def get_winning_cards(self):
        return self.winning_cards
    
    def get_turn_number(self):
        return self.turn_number
    
    def set_turn_number(self, turn_number):
        self.turn_number = turn_number

    def get_suggestion_turn_number(self):
        return self.suggestion_turn_number
    
    def set_suggestion_turn_number(self, suggestion_turn_number):
        self.suggestion_turn_number = suggestion_turn_number

    def get_active_suggestion_cards(self):
        return self.active_suggestion_cards
    
    def set_active_suggestion_cards(self, active_suggestion_cards):
        self.active_suggestion_cards = active_suggestion_cards

    def get_suggesting_player(self):
        return self.suggesting_player
    
    def set_suggesting_player(self, suggesting_player):
        self.suggesting_player = suggesting_player
    
    def deal_cards(self):
        # Randomly select the cards to guess, and deal out the remaining cards
        print("\nDealing cards to the players")
        suspect_list = list(Suspect)
        weapon_list = list(Weapon)
        # Get only the room values, not the hallways
        room_list = [room for room in Room if room.value < 22]

        correct_suspect = random.choice(suspect_list)
        print("The suspect to guess is: " + str(correct_suspect) + ", removing them from the pool of cards.")
        self.winning_cards.append(correct_suspect)
        suspect_list.remove(correct_suspect)

        correct_weapon = random.choice(weapon_list)
        print("The weapon to guess is: " + str(correct_weapon) + ", removing it from the pool of cards.")
        self.winning_cards.append(correct_weapon)
        weapon_list.remove(correct_weapon)

        correct_room = random.choice(room_list)
        print("The room to guess is: " + str(correct_room) + ", removing it from the pool of cards.")
        self.winning_cards.append(correct_room)
        room_list.remove(correct_room)

        # Combine the three catagories into one deck, and shuffle it
        remaining_cards = []
        remaining_cards.extend(suspect_list)
        remaining_cards.extend(weapon_list)
        remaining_cards.extend(room_list)
        random.shuffle(remaining_cards)

        # Deal cards to players
        players = self.get_players()
        num_of_players = len(players)
        index = 0
        for card in remaining_cards:
            players[index].give_card(card)
            if index < (num_of_players-1):
                index = index + 1
            else:
                index = 0
        for player in players:
            print("\nPlayer " + str(player.get_name()) + " now has cards: " + str(player.get_cards()))


    def set_player_positions(self):
        # Assign each player a character and starting position
        #suspect_list = list(Suspect)
        room_list = list(Room)
        players = self.get_players()
        hallway_offset = 9
        index = 0

        print("\nSetting Player Positions")

        for player in players:
            #character = suspect_list[index]
            #player.set_character(character)
            player.set_position(room_list[index+hallway_offset])
            index = index + 1
            player.set_turn_order_number(index)

            print("\nPlayer " + str(player.get_name()) + " will play as " + str(player.get_character()) + ", start in " + str(player.get_position()) + ", and have turn order number " + str(player.get_turn_order_number()))

        # Can use Player.set_position function
        # Assign weapons to rooms
        pass