import clue_game_logic
import clue_messaging
import pickle
import socket
import time # TODO Remove this

# Global dictionary to store ongoing games
ongoing_games = {}

'''
Functions for handling game-state changes
'''
# Creates a new game_logic object to hold game state info.
# Then adds the creating player to the game they created.
def create_new_game(message, addr):
    global ongoing_games

    print('\nCREATE GAME MESSAGE RECEIVED:')
    print('Creating Player:', message.sender_id)

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


# Adds the player in the message to the game with the ID given in the message.
def join_game(message, addr):
    global ongoing_games

    print('\nJOIN GAME MESSAGE RECEIVED:')
    print('Joining Player:', message.sender_id)
    print('Game ID to Join:', message.game_state_data)

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
            #board_info = ''
            board_info = []
            for player in players:
                #board_info = board_info + ((player.get_name() + "(" + str(player.get_character()) + ") is currently in the " + str(player.get_position()) + "\n"))
                stripped_player = clue_game_logic.Player(player.get_name(), None, [])
                stripped_player.set_character(player.get_character())
                stripped_player.set_position(player.get_position())
                board_info.append(stripped_player)

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

# Updates an existing game_logic object (ongoing game) with new player info from the message.
def update_game_state(message):
    global ongoing_games

    print('\nGAME STATE UPDATE RECEIVED:')
    print('Game Session:', message.sender_id)
    print('Player Data:', message.player_state_data)
    game = ongoing_games[message.sender_id]
    game_turn_number = game.get_turn_number() + 1
    if game_turn_number > 3: # TODO: Make this 3 a 6
        game_turn_number = 1
    game.set_turn_number(game_turn_number)
    players = game.get_players()

    # Update the data for the player who sent the update
    index = 0
    while index < len(players):
        player = players[index]
        if player.get_name() == message.player_state_data.get_name():
            players[index] = message.player_state_data
            break # TODO Maybe get rid of this break
        index = index + 1

    board_info = []
    for player in players:
        stripped_player = clue_game_logic.Player(player.get_name(), None, [])
        stripped_player.set_character(player.get_character())
        stripped_player.set_position(player.get_position())
        stripped_player.set_lost_game(player.get_lost_game())
        board_info.append(stripped_player)

    for player in players:
        print("Player " + str(player.get_name()) + " is now in " + str(player.get_position()))

    index = 0
    for player in players:
        game_state_update =  clue_messaging.Message(clue_messaging.Message_Types.GAME_STATE_UPDATE, game.get_id(), board_info, player)
        send_message(game_state_update, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
        print("Sent update to " + player.get_name())
        index = index + 1
        time.sleep(.5)

    index = 0
    turn_notification_sent = False
    while not turn_notification_sent:
        for player in players:
            if player.get_turn_order_number() == game_turn_number:
                        if player.get_lost_game() == True:
                            print("Skipping " + player.get_name() + " because they have lost")
                            game_turn_number = game.get_turn_number() + 1
                            if game_turn_number > 3: # TODO: Make this 3 a 6
                                game_turn_number = 1
                            game.set_turn_number(game_turn_number)
                        else:
                            turn_notification =  clue_messaging.Message(clue_messaging.Message_Types.YOUR_TURN_NOTIFICATION, game.get_id(), board_info, player)
                            send_message(turn_notification, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
                            turn_notification_sent = True
                            print("Sent turn notification to " + player.get_name())
            index = index + 1

# Handles server-side logic for when a player makes an accusation.
def handle_accusation_action(message):
    global ongoing_games

    print('\nACCUSATION ACTION MESSAGE RECEIVED:')
    print('Game Session:', message.sender_id)
    print('Player Data:', message.player_state_data)
    print('Their Guess: ' + str(message.game_state_data))

    game = ongoing_games[message.sender_id]
    winning_cards = game.get_winning_cards()
    if message.game_state_data == winning_cards:
        print("*** They won!")
        index = 0
        players = game.get_players()
        for player in players:
            if player.get_name() == message.player_state_data.get_name():
                you_won_notification = clue_messaging.Message(clue_messaging.Message_Types.YOU_WON_NOTIFICATION, game.get_id(), None, player.get_name())
                send_message(you_won_notification, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
            else:
                game_over_notification = clue_messaging.Message(clue_messaging.Message_Types.GAME_OVER_NOTIFICATION, game.get_id(), None, message.player_state_data.get_name())
                send_message(game_over_notification, player.get_address()[0], (12346+index)) # TODO: Fix port weirdness
            index = index + 1
        del ongoing_games[message.sender_id]
        print("Game removed from ongoing games. \n\nOngoing games: " + str(ongoing_games))
    else:
        print("*** They lost!")
        # Set the losing player's lost_game value to true
        message.player_state_data.set_lost_game(True)
        update_game_state(message)


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


# Listen for and receive messages from clients and call function to process them
def receive_message(host='localhost', port=12345):
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
                

# Validate message type, and pass to correct handling functions
def process_message(message, addr):
    if (message.message_type == clue_messaging.Message_Types.CREATE_GAME):
        create_new_game(message, addr)

    elif (message.message_type == clue_messaging.Message_Types.JOIN_GAME):
        join_game(message, addr)

    elif (message.message_type == clue_messaging.Message_Types.GAME_STATE_UPDATE):
        update_game_state(message)

    elif (message.message_type == clue_messaging.Message_Types.ACCUSATION_ACTION):
        handle_accusation_action(message)

    else:
        print("Error, unknown message type received")


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
