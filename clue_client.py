import clue_messaging
import pickle
import socket
import time
import threading
# TODO: Replace clue_game_logic with an interface that provides less visibility
import clue_game_logic

room_coordinates = {
    clue_game_logic.Room.LOUNGE: (4, 4),
    clue_game_logic.Room.HALL: (4, 2),
    clue_game_logic.Room.STUDY: (4, 0),
    clue_game_logic.Room.LIBRARY: (2, 0),
    clue_game_logic.Room.BILLIARD_ROOM: (2, 2),
    clue_game_logic.Room.DINING_ROOM: (2, 4),
    clue_game_logic.Room.CONSERVATORY: (0, 0),
    clue_game_logic.Room.BALLROOM: (0, 2),
    clue_game_logic.Room.KITCHEN: (0, 4),
    clue_game_logic.Room.HALLWAY_CONS_BALR: (0, 1),
    clue_game_logic.Room.HALLWAY_BALR_KITC: (0, 3),
    clue_game_logic.Room.HALLWAY_CONS_LIBR: (1, 0),
    clue_game_logic.Room.HALLWAY_LIBR_STDY: (3, 0),
    clue_game_logic.Room.HALLWAY_HALL_LOUG: (4, 3),
    clue_game_logic.Room.HALLWAY_DINR_LOUG: (3, 4),
    clue_game_logic.Room.HALLWAY_BALR_BILR: (1, 2),
    clue_game_logic.Room.HALLWAY_KITC_DINR: (1, 4),
    clue_game_logic.Room.HALLWAY_LIBR_BILR: (2, 1),
    clue_game_logic.Room.HALLWAY_BILR_DINR: (2, 3),
    clue_game_logic.Room.HALLWAY_BILR_HALL: (3, 2),
    clue_game_logic.Room.HALLWAY_STDY_HALL: (4, 1)
}

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    # If the value is not found, return None or raise an exception
    return None

'''
Functions for displaying GUI elements
'''
def show_main_menu():
    # Create and display GUI elements for the main menu
    # Should include a button for "Create New Game" and a button for "Join Game"

    # Text based version
    print("Welcome to Clue!")
    print("Do you want to create a new game or join an existing one?")
    print("1. Create a new game")
    print("2. Join an existing game")

    while True:
        option = input("Enter your choice (1 or 2): ")
        if option in ('1', '2'):
            return option
        else:
            print("Invalid choice. Please enter 1 or 2.")

def show_create_game_popup():
    global player_name
    # Create and display GUI elements for the pop-up that appears after you select "Join Game"
    # Should include a space to ender in the game ID of the game you want to join

    # Text based version
    player_name = input("Enter your name: ")

def show_join_game_popup():
    global player_name
    # Create and display GUI elements for the pop-up that appears after you select "Join Game"
    # Should include a space to ender in the game ID of the game you want to join

    # Text based version
    player_name = input("Enter your name: ")
    game_id = input("Enter the ID of the game you want to join: ")
    print("Connecting...")
    return game_id

def show_lobby_menu():
    # Create and display GUI elements for the lobby menu
    # Should include a list of players in the game and some sort of "Start" or "Ready Up" button
    # Should display game ID
    pass

def show_loading_screen(message):
    # Create and display a generic loading page with a message
    pass

def show_game_board():
    # Create and display GUI elements for the game board
    # Should include player/item positions and the players cards
    pass

def update_game_board():
    # Update the positions of items and characters on the board
    pass

def show_your_turn_popup(message):
    # Create and display GUI elements for the pop-up that appears when it is your turn to move
    pass

def show_victory_popup():
    # Create and display GUI elements for the victory pop-up that appears when you have won
    pass

def show_game_over_popup():
    # Create and display GUI elements for the game over pop-up that appears when you have lost
    pass

'''
Functions for handling user actions
'''
def create_new_game():
    # Call show_loading_screen
    # Generate a new game request message and call send_message
    pass

def join_game():
    # Call show_loading_screen
    # Generate a new join game request message and call send_message
    pass

def handle_player_action():
    # This may need to get broken out into several functions
    pass

def enable_controls():
    # Make the action buttons selectable. To be called when it is the players turn
    pass

def disable_controls():
    # Make the action buttons unselectable. To be called when it is the end of a players turn
    pass

'''
Functions for messaging
'''
def send_message(message, host='localhost', port=12345):
    # Apply any additional formatting and send message to server
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

def receive_message(host='localhost', port=12346):
    # Process message received from server and call functions to update the GUI accordingly
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    # Receive the message length
                    message_length_bytes = conn.recv(4)
                    message_length = int.from_bytes(message_length_bytes, byteorder='big')
                    # Receive the serialized message
                    serialized_message = b''
                    while len(serialized_message) < message_length:
                        serialized_message += conn.recv(message_length - len(serialized_message))
                    # Deserialize the message object using pickle
                    message = pickle.loads(serialized_message)
                    process_message(message)
        except:
            # TODO: Replace port stuff with with a permanent solution
            print("Port in use, trying next port")
            port = port + 1

def process_message(message):
    global game_id
    try:
        if (message.message_type == clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE):
            game_id = message.sender_id
            # TODO: Format this data into a message showing only the Game ID and list of players in the lobby
            print('\nReceived message:')
            print('Type:', message.message_type)
            print('Sender ID:', message.sender_id)
            print('Game State Data:', message.game_state_data)
            print('Player Data:', message.player_state_data)

        elif (message.message_type == clue_messaging.Message_Types.YOUR_TURN_NOTIFICATION):
            print('\nIts your turn!')
            player_state = message.player_state_data
            # Process where the player can move and present their options for moving
            position = player_state.get_position()
            print('You are currently in the ' + str(position))
            print('You can move to:')
            x = room_coordinates[position][0]
            y = room_coordinates[position][1]
            # TODO: This can be a loop
            # TODO: Check if a character is already in any of these hallways
            # TODO: Add secret passages
            choices = {}
            index = 1
            adjacent_cord = (x-1,y)
            room_name = get_key_by_value(room_coordinates, adjacent_cord)
            if(room_name is not None):
                print(str(index) + " : " + room_name.name)
                choices[index] = room_name
                index = index + 1
            adjacent_cord = (x+1,y)
            room_name = get_key_by_value(room_coordinates, adjacent_cord)
            if(room_name is not None):
                print(str(index) + " : " + room_name.name)
                choices[index] = room_name
                index = index + 1
            adjacent_cord = (x,y-1)
            room_name = get_key_by_value(room_coordinates, adjacent_cord)
            if(room_name is not None):
                print(str(index) + " : " + room_name.name)
                choices[index] = room_name
                index = index + 1
            adjacent_cord = (x,y+1)
            room_name = get_key_by_value(room_coordinates, adjacent_cord)
            if(room_name is not None):
                print(str(index) + " : " + room_name.name)
                choices[index] = room_name
                index = index + 1

            print(choices)
            new_position = None
            while new_position is None:
                given_position = input("Enter the number of the room where would you like to move: ")
                print(choices[int(given_position)])
                if choices[int(given_position)] in clue_game_logic.Room:
                    new_position = choices[int(given_position)]
                else:
                    print("That is not a valid room, try again.")

            player_state.set_position(new_position)
            create_game_message =  clue_messaging.Message(clue_messaging.Message_Types.GAME_STATE_UPDATE, game_id, None, player_state)
            send_message(create_game_message)

            # If the player is in a room (not a hallway), give them the option to suggest
            if new_position.value < 22:
                # print('Make a suggestion:')
                # TODO: List players and weapons
                # TODO: Let the player select a player and weapon to suggest
                pass
            else:
                print('You cannot make a suggestion from a hallway')

        elif (message.message_type == clue_messaging.Message_Types.GAME_STATE_UPDATE):
            # TODO: Format this data into a message listing all player's new positions,
            #       and showing the client player's character and list of cards
            print('\nReceived message:')
            print('Type:', message.message_type)
            print('Sender ID:', message.sender_id)
            print('Game State Data:\n', message.game_state_data)
            print('Player Data:', message.player_state_data)

        else:
            print('WARN: Bad message type received')

        # TODO: If the GAME_STATE_UPDATE is not sufficient, add other message types to handle players taking their turns
            
    except Exception as e:
        print("Error occurred while processing message:", e)
    # TODO: Set a flag here in the message is of the start game type

# Global values
player_name = ""
game_id = 0

'''
Main
'''
def main():

    # Start receiving messages in a separate thread
    receive_message_thread = threading.Thread(target=receive_message)
    receive_message_thread.daemon = True
    receive_message_thread.start()

    # TODO: This is a temp sleep to ensure initial logging in receive_message_thread doesn't overlap initial prompts
    time.sleep(1)
    
    choice = show_main_menu()
    if choice == '1':
        show_create_game_popup()
        create_game_message =  clue_messaging.Message(clue_messaging.Message_Types.CREATE_GAME, player_name, None, None)
        send_message(create_game_message)
        # Call function to create a new game
    else:
        game_id = show_join_game_popup()
        create_game_message =  clue_messaging.Message(clue_messaging.Message_Types.JOIN_GAME, player_name, int(game_id), None)
        send_message(create_game_message)

    while True:
        time.sleep(2)

if __name__ == "__main__":
    main()