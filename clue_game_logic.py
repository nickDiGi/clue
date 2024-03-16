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
        self.cards = cards
        self.turn_number = None
        self.character = None
        self.position = None

    def get_name(self):
        return self.name

    def give_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

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
        print("Dealing cards to the players")
        suspect_list = list(Suspect)
        weapon_list = list(Weapon)
        room_list = list(Room)

        correct_suspect = random.choice(suspect_list)
        print("The suspect to guess is: " + str(correct_suspect) + ", removing them from the pool of cards.")
        suspect_list.remove(correct_suspect)
        print("Remaining suspects: " + str(suspect_list))

        correct_weapon = random.choice(weapon_list)
        print("The weapon to guess is: " + str(correct_weapon) + ", removing it from the pool of cards.")
        weapon_list.remove(correct_weapon)
        print("Remaining weapons: " + str(weapon_list))

        correct_room = random.choice(room_list)
        print("The room to guess is: " + str(correct_room) + ", removing it from the pool of cards.")
        room_list.remove(correct_room)
        print("Remaining rooms: " + str(room_list))

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
            print("Player " + str(player.get_name()) + " now has cards: " + str(player.get_cards()))


    def set_player_positions(self):
        # Assign each player a random position
        # Can use Player.set_position function
        # Assign weapons to rooms
        pass