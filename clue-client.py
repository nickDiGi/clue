import socket
import pickle
import threading
from enum import Enum

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
    # Create and display GUI elements for the pop-up that appears after you select "Join Game"
    # Should include a space to ender in the game ID of the game you want to join

    # Text based version
    return input("Enter your name: ")

def show_join_game_popup():
    # Create and display GUI elements for the pop-up that appears after you select "Join Game"
    # Should include a space to ender in the game ID of the game you want to join
    pass

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
        print("Sent")
    except Exception as e:
        print("Error occurred while sending message:", e)

def process_message(host='localhost', port=12346):
    # Process message received from server and call functions to update the GUI accordingly
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
                print('Received message:')
                print('Type:', message.message_type)
                print('Sender ID:', message.sender_id)
                print('Data:', message.data)

'''
Main
'''
def main():

    # Start receiving messages in a separate thread
    receive_message_thread = threading.Thread(target=process_message)
    receive_message_thread.daemon = True
    receive_message_thread.start()

    while True: # TODO: This loop is for testing and demonstration
        choice = show_main_menu()
        if choice == '1':
            player_name = show_create_game_popup()
            create_game_message =  Message(Message_Types.CREATE_GAME, player_name, None)
            send_message(create_game_message)
            # Call function to create a new game
        else:
            create_game_message =  Message(Message_Types.JOIN_GAME, "Temp-Name", 95417)
            send_message(create_game_message)

if __name__ == "__main__":
    main()