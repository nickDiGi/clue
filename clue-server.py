import random
import socket
from enum import Enum

import pickle

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
class Game_Logic:
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

# Global dictionary to store ongoing games
ongoing_games = {}

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
def send_message(message, host, port=12346):
    # Apply any additional formatting and send message to client
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            # Serialize the message object using pickle
            serialized_message = pickle.dumps(message)
            # Prefix the serialized message with its length
            message_length = len(serialized_message)
            s.sendall(message_length.to_bytes(4, byteorder='big'))
            s.sendall(serialized_message)
        print("Sent")
    except Exception as e:
        print("Error occurred while sending message:", e)

def process_message(host='localhost', port=12345):
    # Process message received from client and call functions to handle accordingly
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)

                # Receive the message length
                message_length_bytes = conn.recv(4)
                message_length = int.from_bytes(message_length_bytes, byteorder='big')
                # Receive the serialized message
                serialized_message = b''
                while len(serialized_message) < message_length:
                    serialized_message += conn.recv(message_length - len(serialized_message))
                # Deserialize the message object using pickle
                message = pickle.loads(serialized_message)
                if (message.message_type == Message_Types.CREATE_GAME):
                    # Create game
                    game = Game_Logic(message.sender_id, addr)
                    # Add game to the collection of games, with it's ID as it's key
                    ongoing_games[game.get_id()] = game
                    print("Added player " + message.sender_id + " to game with lobby ID " + str(game.get_id()))
                    player_names = []
                    for player in game.get_players():
                            player_names.append(player.get_name())
                    create_game_response =  Message(Message_Types.LOBBY_ROSTER_UPDATE, None, player_names)
                    send_message(create_game_response, 'localhost')
                    print("Sent create game response")

                elif (message.message_type == Message_Types.JOIN_GAME):
                    try:
                        game = ongoing_games[message.data]
                        print("That game exists!")
                        game.add_player(addr, message.sender_id)
                        for player in game.get_players():
                            print(player.get_address())
                    except:
                        print("Sorry, we couldn't find that game")
                else:
                    print("Error, unknown message type received")

'''
Main
'''
def main():
    # Start the server to receive the message
    print("Server Started")
    process_message()
    pass

if __name__ == "__main__":
    main()