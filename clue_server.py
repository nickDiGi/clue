import clue_game_logic
import clue_messaging
import pickle
import socket
import time # TODO Remove this

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
# TODO: Replace port stuff with with a permanent solution
def send_message(message, host, port):
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

def receive_message(host='localhost', port=12345):
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
                process_message(message, addr)

# Commented out HTTP code because I was having trouble running it an did not understand its purpose.
# TODO: Get a demo of the code from Nicole 

# class RequestHandler(BaseHTTP):
    def do_POST(self):
        if self.path == '/select_character':
            content_length = int(self.headers['Content-Length'])
            post_data = self-rfile.read(content_length)
            selected_character = pickle.loads(post_data)
            print("Selected character:", selected_character)
            self.send_response(200)
            self.send_header(Content-type, 'text/plain')
            self.end_header()
            self.wfile.write(b'Character selection successful')
        else:
            self.send_response(404)
            self.send_header(Content-type, 'text/plain')
            self.end_header()
            self.wfile.write(b'Not found')

# class ThreadedHTTP(ThreadedMixIn, HTTPServer):
    pass

# def run_server():
    server_address = ('', 8000)
    server = ThreadedHTTP(server_address, RequestHandler)
    print('Starting server...')
    server.serve_forever()
                

def process_message(message, addr):
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
        create_game_response =  clue_messaging.Message(clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE, game.get_id(), player_names, None)
        # TODO: Replace port stuff with with a permanent solution
        index = 0
        for player in game.get_players():
            send_message(create_game_response, player.get_address()[0], (12346+index))
            print("Sent lobby update to " + player.get_name())
            index = index + 1

    elif (message.message_type == clue_messaging.Message_Types.JOIN_GAME):
        try:
            game = ongoing_games[message.game_state_data]
            print("Game Found Matching Given ID")
            game.add_player(message.sender_id, addr)
            print("Added player " + message.sender_id + " to game with lobby ID " + str(game.get_id()))
            player_names = []
            for player in game.get_players():
                    player_names.append(player.get_name())
            print("Players now the lobby: " + str(player_names))
            create_game_response =  clue_messaging.Message(clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE, game.get_id(), player_names, None)
            # TODO: Replace port stuff with with a permanent solution
            index = 0
            for player in game.get_players():
                send_message(create_game_response, player.get_address()[0], (12346+index))
                print("Sent lobby update to " + player.get_name())
                index = index + 1

            # TODO: Make this happen after a start game message is received
            if len(player_names) == 3:
                # Deal cards and set starting positions
                game.deal_cards()
                game.set_player_positions()

                # Parse list of players to grab info about their character and where they are on the board
                players = game.get_players()
                board_info = ''
                for player in players:
                    board_info = board_info + ((player.get_name() + " is playing as " + str(player.get_character()) + " and starting in " + str(player.get_position()) + "\n"))

                # Send message to each player with the positions of other players and their own player info
                index = 0
                for player in players:
                    print("\n")
                    print(player)
                    game_state_update =  clue_messaging.Message(clue_messaging.Message_Types.GAME_STATE_UPDATE, game.get_id(), board_info, player)
                    send_message(game_state_update, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
                    print("Sent update to " + player.get_name())
                    # Notify the player who's turn it is that it is their turn
                    if player.turn_order_number == 1:
                        time.sleep(.5) # TODO : Add threading and remove this
                        turn_notification =  clue_messaging.Message(clue_messaging.Message_Types.YOUR_TURN_NOTIFICATION, game.get_id(), board_info, player)
                        send_message(turn_notification, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
                        print("Sent turn notification to " + player.get_name())
                    index = index + 1
                    time.sleep(.5) # TODO : Add threading and remove this
                    
        except Exception as e:
            print("Sorry, we couldn't find that game: ", e)
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
    receive_message()
    # run_server()

if __name__ == "__main__":
    main()
