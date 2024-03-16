import clue_game_logic
import clue_messaging
import pickle
import socket

'''
Functions for handling game-state changes
'''
def create_new_game():
    # Generate a new game logic handler and call its init
    # Add the game logic hander to the list of current game logic handlers
    # Generate message with Game_Session game_id to send to client
    pass

def join_game(game_id, player_id):
    # Using the given game_id, find the game in the list of current games, and add the player to the roster
    # Create a message notifying players in that game that someone has joined, and call send_message
    # Call Game_Session functions to add_player(s), and once the lobby is full,
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
                print('\nConnected by', addr)

                # Receive the message length
                message_length_bytes = conn.recv(4)
                message_length = int.from_bytes(message_length_bytes, byteorder='big')
                # Receive the serialized message
                serialized_message = b''
                while len(serialized_message) < message_length:
                    serialized_message += conn.recv(message_length - len(serialized_message))
                # Deserialize the message object using pickle
                message = pickle.loads(serialized_message)
                if (message.message_type == clue_messaging.Message_Types.CREATE_GAME):
                    # Create game
                    game = clue_game_logic.Game_Session(message.sender_id, addr)
                    # Add game to the collection of games, with it's ID as it's key
                    ongoing_games[game.get_id()] = game
                    print("Added player " + message.sender_id + " to game with lobby ID " + str(game.get_id()))
                    player_names = []
                    for player in game.get_players():
                            player_names.append(player.get_name())
                    print("Players now the lobby: " + str(player_names))
                    create_game_response =  clue_messaging.Message(clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE, game.get_id(), player_names)
                    for player in game.get_players():
                        send_message(create_game_response, player.get_address()[0])
                        print("Sent lobby update to " + player.get_name())

                elif (message.message_type == clue_messaging.Message_Types.JOIN_GAME):
                    try:
                        game = ongoing_games[message.data]
                        print("Game Found Matching Given ID")
                        game.add_player(message.sender_id, addr)
                        print("Added player " + message.sender_id + " to game with lobby ID " + str(game.get_id()))
                        player_names = []
                        for player in game.get_players():
                                player_names.append(player.get_name())
                        print("Players now the lobby: " + str(player_names))
                        create_game_response =  clue_messaging.Message(clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE, game.get_id(), player_names)
                        for player in game.get_players():
                            send_message(create_game_response, player.get_address()[0])
                            print("Sent lobby update to " + player.get_name())
                    except:
                        print("Sorry, we couldn't find that game")
                else:
                    print("Error, unknown message type received")

# Global dictionary to store ongoing games
ongoing_games = {}

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