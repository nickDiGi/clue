import sqlite3

class Player:
    def __init__(self, name, address, cards):
        self.name = name
        self.address = address
        self.cards = cards
        self.turn_order_number = None
        self.character = None
        self.position = None
        self.lost_game = False

    # Other methods omitted for brevity

# Connect to SQLite database
conn = sqlite3.connect('players.db')
cursor = conn.cursor()

# Create a table to store Player objects
cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    name TEXT,
                    address TEXT,
                    cards TEXT,
                    turn_order_number INTEGER,
                    character TEXT,
                    position TEXT,
                    lost_game INTEGER
                )''')

# Save a Player object to the database
def save_player(player):
    cursor.execute('''INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (player.name, player.address, ','.join(player.cards), 
                    player.turn_order_number, player.character, 
                    player.position, int(player.lost_game)))
    conn.commit()

# Retrieve Player objects from the database
def load_players():
    cursor.execute('''SELECT * FROM players''')
    players = []
    for row in cursor.fetchall():
        name, address, cards_str, turn_order_number, character, position, lost_game = row
        cards = cards_str.split(',')
        player = Player(name, address, cards)
        player.turn_order_number = turn_order_number
        player.character = character
        player.position = position
        player.lost_game = bool(lost_game)
        players.append(player)
    return players

# Example usage:
player1 = Player('Alice', '123 Main St', ['Card1', 'Card2'])
save_player(player1)

player2 = Player('Bob', '456 Elm St', ['Card3', 'Card4'])
save_player(player2)

loaded_players = load_players()
for player in loaded_players:
    print(player.name, player.address, player.cards)

# Close the database connection
conn.close()
