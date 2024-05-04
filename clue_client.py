import clue_messaging
import pickle
import socket
import time
import threading

# TODO: Replace clue_game_logic with an interface that provides less visibility
import clue_game_logic

import pygame

from frontend.lobby import Lobby
from frontend.game import Game
from frontend.client import MainMenu
from frontend.test_lobby import LobbyScreen
from frontend.choose_character import ChooseCharacter
from frontend.constants import *

# Global values
player_name = ""
game_id = 0
turn_ended = False
moved_this_turn = False
player_info = []  # An array that will contain the players in the game and their data

# Constants
HALLWAY_LIMIT = 22

# Mapping used to find available moves for a player
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
    clue_game_logic.Room.HALLWAY_STDY_HALL: (4, 1),
}

# Dictionary to map suspect names to their enum values
suspect_mapping = {suspect.name: suspect for suspect in clue_game_logic.Suspect}
# Dictionary to map weapon names to their enum values
weapon_mapping = {weapon.name: weapon for weapon in clue_game_logic.Weapon}
# Dictionary to map room names to their enum values
room_mapping = {room.name: room for room in clue_game_logic.Room}

"""
Helper Functions
"""


def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    # If the value is not found, return None or raise an exception
    return None


"""
Functions for displaying GUI elements
"""


# Create and display GUI elements for the main menu
# Should include a button for "Create New Game" and a button for "Join Game"
def show_main_menu():
    # Text based version
    print("Welcome to Clue!")
    print("Do you want to create a new game or join an existing one?")
    print("1. Create a new game")
    print("2. Join an existing game")

    while True:
        option = input("Enter your choice (1 or 2): ")
        if option in ("1", "2"):
            return option
        else:
            print("Invalid choice. Please enter 1 or 2.")
    # End text based version


# Create and display GUI elements for the pop-up that appears after you select "Join Game"
# Should include a space to ender in the game ID of the game you want to join
def show_create_game_popup():
    global player_name
    # TODO: Connect GUI here

    # Text based version
    player_name = input("Enter your name: ")
    # End text based version


# Create and display GUI elements for the pop-up that appears after you select "Join Game"
# Should include a space to ender in the game ID of the game you want to join
def show_join_game_popup():
    global player_name
    # TODO: Connect GUI here

    # Text based version
    player_name = input("Enter your name: ")
    game_id = input("Enter the ID of the game you want to join: ")
    print("Connecting...")
    return game_id
    # End text based version


# Create and display GUI elements for the lobby menu
# Should include a list of players in the game a "Start" or "Ready Up" button and the game ID
def show_lobby_menu(lobby_roster):
    global game_id
    global lobby_screen

    lobby_screen.add_player(lobby_roster)

    # Text based version
    print("\nA NEW PLAYER HAS JOINED THE LOBBY!")
    print("In Lobby:", lobby_roster)
    print("Lobby ID:", game_id)
    # TODO: Add a ready up button/option
    # End text based version


# Update the positions of items and characters on the board
def update_game_board(new_player_info):
    global player_info
    lobby_screen.running = False

    # Text based version
    if not player_info:
        print("\nTHE GAME HAS STARTED")
    else:
        print("\nPLAYERS HAVE MOVED!")
    player_info = new_player_info
    for player in player_info:
        print(
            (player.get_character().name)
            + " ("
            + (player.get_name())
            + ") is in the "
            + (player.get_position().name)
        )
        if player.get_lost_game():
            print(
                "*** "
                + (player.get_character().name)
                + " ("
                + (player.get_name())
                + ") made an incorrect accusation. They have lost the game and cannot move."
            )
    # End text based version


# Create and display GUI elements for the pop-up that appears when it is your turn to move
def show_your_turn_popup(player_state):
    # TODO: Connect GUI here
    game_board.buttons_enabled = True

    # Text based version
    while not turn_ended:
        print("\nITS YOUR TURN!")
        print("1. Move")
        print("2. Suggest")
        print("3. Accuse")
        print("4. View Cards")
        print("5. End Turn")
        action = input("Enter the number of the action you would like to take: ")
        action_options.get(action, show_error_popup)(player_state)
    # End text based version


# Create and display GUI elements for the victory pop-up that appears when you have won
def show_victory_popup():
    # TODO: Connect GUI here
    pass


# Create and display GUI elements for the game over pop-up that appears when you have lost
def show_game_over_popup():
    # TODO: Connect GUI here
    pass


# Create and display GUI elements for an error message pop-up
def show_error_popup(player_state):
    # TODO: Connect GUI here

    # Text based version
    print("Invalid input, please try again.")
    # End text based version


# Display the players cards
def show_cards(player_state):
    cards = ", ".join(card.name for card in player_state.get_cards())
    # TODO: Connect GUI here

    # Text based version
    print("Your cards are: " + cards)
    # End text based version


# Make the action buttons selectable. To be called when it is the players turn
def enable_controls():
    pass


# Make the action buttons unselectable. To be called when it is the end of a players turn
def disable_controls():
    pass


"""
Functions for handling user actions
"""


def create_game(player_name, character):
    create_game_message = clue_messaging.Message(
        clue_messaging.Message_Types.CREATE_GAME, player_name, None, character
    )
    connect_to_server()
    send_message(create_game_message)


def join_game(player_name, game_id, character):
    join_game_message = clue_messaging.Message(
        clue_messaging.Message_Types.JOIN_GAME, player_name, int(game_id), character
    )
    connect_to_server()
    send_message(join_game_message)


# Process where the player can move and present their options for moving
def handle_move(player_state):
    global turn_ended
    global moved_this_turn

    if moved_this_turn:
        print("You have already moved this turn.")
    else:
        position = player_state.get_position()
        print("You are currently in the " + str(position.name))
        print("You can move to:")
        x = room_coordinates[position][0]
        y = room_coordinates[position][1]

        # TODO: Add secret passages
        choices = {}
        index = 1
        adjacent_cord = (x - 1, y)
        room_name = get_key_by_value(room_coordinates, adjacent_cord)
        # Get the possible rooms the player can move to
        if room_name is not None:
            print(str(index) + " : " + room_name.name)
            choices[index] = room_name
            index = index + 1
        adjacent_cord = (x + 1, y)
        room_name = get_key_by_value(room_coordinates, adjacent_cord)
        if room_name is not None:
            print(str(index) + " : " + room_name.name)
            choices[index] = room_name
            index = index + 1
        adjacent_cord = (x, y - 1)
        room_name = get_key_by_value(room_coordinates, adjacent_cord)
        if room_name is not None:
            print(str(index) + " : " + room_name.name)
            choices[index] = room_name
            index = index + 1
        adjacent_cord = (x, y + 1)
        room_name = get_key_by_value(room_coordinates, adjacent_cord)
        if room_name is not None:
            print(str(index) + " : " + room_name.name)
            choices[index] = room_name
            index = index + 1

        # Get the players choice of move
        new_position = None
        while new_position is None:
            given_position = input(
                "Enter the number of the room where would you like to move: "
            )
            if choices[int(given_position)] in clue_game_logic.Room:
                new_position = choices[int(given_position)]
                for player in player_info:
                    # Check if the room is a hallway, and if another player is blocking it
                    if (
                        player.get_position() == new_position
                        and new_position.value >= HALLWAY_LIMIT
                    ):
                        print("That position is already occupied! try again.")
                        new_position = None
                        break
            else:
                print("That is not a valid room, try again.")
        moved_this_turn = True

        player_state.set_position(new_position)


# Let the player choose a suspect, weapon, and room
def choose_cards(choose_room):
    suspect_list = list(clue_game_logic.Suspect)
    suspects = ", ".join(suspect.name for suspect in suspect_list)
    weapon_list = list(clue_game_logic.Weapon)
    weapons = ", ".join(weapon.name for weapon in weapon_list)
    room_list = [room for room in clue_game_logic.Room if room.value < 22]
    rooms = ", ".join(room.name for room in room_list)

    chosen_suspect = ""
    while not chosen_suspect:
        print("The possible suspects are: " + suspects)
        chosen_suspect = input("Enter the name of the suspect who did it: ")
        chosen_suspect = chosen_suspect.upper()
        if chosen_suspect not in [suspect.name for suspect in suspect_list]:
            chosen_suspect = ""
            print("Invalid suspect, try again.")

    chosen_weapon = ""
    while not chosen_weapon:
        print("The possible weapons are: " + weapons)
        chosen_weapon = input("Enter the name of the weapon they used: ")
        chosen_weapon = chosen_weapon.upper()
        if chosen_weapon not in [weapon.name for weapon in weapon_list]:
            chosen_weapon = ""
            print("Invalid weapon, try again.")

    if choose_room:
        chosen_room = ""
        while not chosen_room:
            print("The possible rooms are: " + rooms)
            chosen_room = input("Enter the name of the room it was done in: ")
            chosen_room = chosen_room.upper()
            if chosen_room not in [room.name for room in room_list]:
                chosen_room = ""
                print("Invalid room, try again.")
        chosen_cards = [
            suspect_mapping.get(chosen_suspect),
            weapon_mapping.get(chosen_weapon),
            room_mapping.get(chosen_room),
        ]
    else:
        chosen_cards = [
            suspect_mapping.get(chosen_suspect),
            weapon_mapping.get(chosen_weapon),
        ]

    return chosen_cards


# Handle collecting user input for a suggestion
def handle_suggest(player_state):
    global turn_ended
    global game_board

    # If the player is in a room (not a hallway), give them the option to suggest
    if player_state.get_position().value >= HALLWAY_LIMIT:
        print("You cannot make a suggestion from a hallway.")
    else:
        chosen_cards = choose_cards(False)
        chosen_cards.append(player_state.get_position())
        turn_ended = True
        suggest_action_message = clue_messaging.Message(
            clue_messaging.Message_Types.SUGGESTION_ACTION,
            game_id,
            chosen_cards,
            player_state,
        )
        game_board.buttons_enabled = False
        send_message(suggest_action_message)


# Handle collecting user input for the accusation and sending it to the server
def handle_disprove(active_suggestion_cards, suggesting_player, player_state):
    global game_board

    # If you are asked to disprove your own suggestion, that means no one else could
    if suggesting_player.get_name() == player_state.get_name():
        print("None of the other players could disprove your suggestion!")
        # Send a game update with no new moves to signal the server to go to the next player
        print(
            "Sending a do-nothing game update with: " + player_state.get_position().name
        )
        game_state_update = clue_messaging.Message(
            clue_messaging.Message_Types.GAME_STATE_UPDATE, game_id, None, player_state
        )
        game_board.buttons_enabled = False
        send_message(game_state_update)
    else:
        print(
            "\nA SUGGESTION WAS MADE BY "
            + suggesting_player.get_name().upper()
            + ": "
            + str(active_suggestion_cards)
        )
        # Convert arrays to sets to remove duplicate elements
        player_cards = set(player_state.get_cards())
        suggestion_cards = set(active_suggestion_cards)

        # Find the intersection of the sets
        common_items = list(player_cards.intersection(suggestion_cards))
        if not common_items:
            print("You do not have the cards to disprove it, moved to the next player.")
            disprove_suggestion_message = clue_messaging.Message(
                clue_messaging.Message_Types.DISPROVE_SUGGESTION_ACTION,
                game_id,
                None,
                player_state,
            )
            game_board.buttons_enabled = False
            send_message(disprove_suggestion_message)
        else:
            cards = ", ".join(card.name for card in common_items)
            chosen_card = ""
            while not chosen_card:
                print("You can disprove the suggestion using you card(s): " + cards)
                chosen_card = input("Enter the name of the card you want to show: ")
                chosen_card = chosen_card.upper()
                if chosen_card not in [card.name for card in active_suggestion_cards]:
                    chosen_card = ""
                    print("Invalid card, try again.")
                else:
                    disprove_suggestion_message = clue_messaging.Message(
                        clue_messaging.Message_Types.DISPROVE_SUGGESTION_ACTION,
                        game_id,
                        chosen_card,
                        player_state,
                    )
                    game_board.buttons_enabled = False
                    send_message(disprove_suggestion_message)             


# Handle collecting user input for the accusation and sending it to the server
def handle_show_card(sender, card, player_state):
    if type(card) == str:
        print(
            player_state.get_name()
            + " showed you their card "
            + card
            + " to disprove your suggestion."
        )
    else:
        print(
            "\n"
            + sender.get_name()
            + " suggested the crime was "
            + str(card)
            + ", but it was disproved by "
            + player_state.get_name()
        )


# Handle collecting user input for the accusation and sending it to the server
def handle_accuse(player_state):
    global turn_ended
    global game_board

    chosen_cards = choose_cards(True)
    turn_ended = True
    accusation_action_message = clue_messaging.Message(
        clue_messaging.Message_Types.ACCUSATION_ACTION,
        game_id,
        chosen_cards,
        player_state,
    )
    game_board.buttons_enabled = False
    send_message(accusation_action_message)


def end_turn(player_state):
    global turn_ended
    global game_board

    turn_ended = True
    game_state_update = clue_messaging.Message(
        clue_messaging.Message_Types.GAME_STATE_UPDATE, game_id, None, player_state
    )
    game_board.buttons_enabled = False
    send_message(game_state_update)


# Maps the above functions to a menu number
action_options = {
    "1": handle_move,
    "2": handle_suggest,
    "3": handle_accuse,
    "4": show_cards,
    "5": end_turn,
}


"""
Functions for messaging
"""


# Connect to the server and listen for messages in a separate thread
def connect_to_server():
    receive_message_thread = threading.Thread(target=receive_message)
    receive_message_thread.daemon = True
    receive_message_thread.start()


# Send a message to the server
# TODO: Use a more permanent solution than a hardcoded host and port
def send_message(message, host="localhost", port=12345):
    # Apply any additional formatting and send message to server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            # Serialize the message object using pickle
            serialized_message = pickle.dumps(message)
            # Prefix the serialized message with its length
            message_length = len(serialized_message)
            s.sendall(message_length.to_bytes(4, byteorder="big"))
            s.sendall(serialized_message)
    except Exception as e:
        print("Error occurred while sending message:", e)


# Listen for incoming messages and pass to process_message for handling
def receive_message(host="localhost", port=12346):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    # Receive the message length
                    message_length_bytes = conn.recv(4)
                    message_length = int.from_bytes(
                        message_length_bytes, byteorder="big"
                    )
                    # Receive the serialized message
                    serialized_message = b""
                    while len(serialized_message) < message_length:
                        serialized_message += conn.recv(
                            message_length - len(serialized_message)
                        )
                    # Deserialize the message object using pickle
                    message = pickle.loads(serialized_message)
                    process_message(message)
        except:
            # TODO: Replace port stuff with with a permanent solution
            port = port + 1


# Verify the message type of the received message, and pass to the correct handling function
def process_message(message):
    global game_id
    global player_info
    global turn_ended
    global moved_this_turn

    try:
        # Show players the list of other players in the lobby, and the lobby ID
        if message.message_type == clue_messaging.Message_Types.LOBBY_ROSTER_UPDATE:
            game_id = message.sender_id
            show_lobby_menu(message.game_state_data)

        # Update the positions of players on the board
        elif message.message_type == clue_messaging.Message_Types.GAME_STATE_UPDATE:
            update_game_board(message.game_state_data)

        # Present the player with their possible actions, and process actions taken
        elif (
            message.message_type == clue_messaging.Message_Types.YOUR_TURN_NOTIFICATION
        ):
            turn_ended = False
            moved_this_turn = False
            show_your_turn_popup(message.player_state_data)

        # Present the player with their options for disproving an active suggestion
        elif (
            message.message_type
            == clue_messaging.Message_Types.DISPROVE_SUGGESTION_ACTION
        ):
            handle_disprove(
                message.game_state_data, message.sender_id, message.player_state_data
            )

        # Show the player the card presented by the other player
        elif message.message_type == clue_messaging.Message_Types.SHOW_CARD_ACTION:
            handle_show_card(
                message.sender_id, message.game_state_data, message.player_state_data
            )

        elif (
            message.message_type == clue_messaging.Message_Types.GAME_OVER_NOTIFICATION
        ):
            print("\n##############################")
            print("## GAME OVER " + message.player_state_data.upper() + " HAS WON ##")
            print("##############################")

        elif message.message_type == clue_messaging.Message_Types.YOU_WON_NOTIFICATION:
            print("\n#########################")
            print("##       YOU WIN       ##")
            print("#########################")

        else:
            print("WARN: Bad message type received.")

    except Exception as e:
        print("Error occurred while processing message:", e)


"""
Main
"""


def main():
    global lobby_screen
    global game_board
    global game_id

    pygame.init()
    player_name = ""
    game_id = -1

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 28)

    main_menu = MainMenu(screen, font)
    choose_character = ChooseCharacter(screen, font)
    lobby_screen = LobbyScreen(screen, font)

    # show_main_menu() OLD TEXT BASED MAIN MENU

    selections = main_menu.menu()
    if len(selections) > 1:
        player_name = selections[1]
        game_id = selections[0]
    else:
        player_name = selections[0]

    character_choice = choose_character.menu()
    print(character_choice)

    # TODO: Fix threading to stop lag
    if game_id == -1:
        message_thread = threading.Thread(target=create_game(player_name, character_choice))
        message_thread.start()
    else:
        message_thread = threading.Thread(target=join_game(player_name, game_id, character_choice))
        message_thread.start()

    while lobby_screen.running:
        lobby_screen.menu()

    game_board = Game(screen, font, player_name, character_choice, game_id)
    game_board.menu()

    # Sleep while waiting for incoming messages
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
