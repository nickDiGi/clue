'''
Functions for displaying GUI elements
'''
def show_main_menu():
    # Create and display GUI elements for the main menu
    # Should include a button for "Create New Game" and a button for "Join Game"
    pass

def show_lobby_menu():
    # Create and display GUI elements for the lobby menu
    # Should include a list of players in the game and some sort of "Start" or "Ready Up" button
    # Should display game ID
    pass

def show_join_game_popup():
    # Create and display GUI elements for the pop-up that appears after you select "Join Game"
    # Should include a space to ender in the game ID of the game you want to join
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
def send_message(message):
    # Apply any additional formatting and send message to server
    pass

def process_message():
    # Process message received from server and call functions to update the GUI accordingly
    pass

'''
Main
'''
def main():
    pass

if __name__ == "__main__":
    main()