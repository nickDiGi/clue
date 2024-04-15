import sqlite3

class GameSession:
    def __init__(self, id, turn_number, winning_cards):
        self.id = id
        self.turn_number = turn_number
        self.winning_cards = winning_cards

class GameSessionDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS game_sessions (
                                id INTEGER PRIMARY KEY,
                                turn_number INTEGER,
                                winning_cards TEXT
                              )''')
        self.conn.commit()

    def insert_game_session(self, game_session):
        sql = '''INSERT INTO game_sessions (turn_number, winning_cards)
                 VALUES (?, ?)'''
        self.cursor.execute(sql, (game_session.turn_number, ','.join(game_session.winning_cards)))
        self.conn.commit()

    def get_game_sessions(self):
        self.cursor.execute("SELECT * FROM game_sessions")
        rows = self.cursor.fetchall()
        game_sessions = []
        for row in rows:
            id, turn_number, winning_cards_str = row
            winning_cards = winning_cards_str.split(',')
            game_sessions.append(GameSession(id, turn_number, winning_cards))
        return game_sessions

    def close(self):
        self.conn.close()

# Create a database instance
db = GameSessionDatabase('game_sessions.db')

# Insert some sample game sessions
game_session1 = GameSession(1, 1, ['Green', 'Revolver', 'Library'])
game_session2 = GameSession(2, 2, ['Mustard', 'Candlestick', 'Lounge'])
game_session3 = GameSession(3, 3, ['Scarlet', 'Dagger', 'Conservatory'])

db.insert_game_session(game_session1)
db.insert_game_session(game_session2)
db.insert_game_session(game_session3)

# Retrieve all game sessions from the database
all_game_sessions = db.get_game_sessions()

# Print retrieved game sessions
for game_session in all_game_sessions:
    print(f"Game Session ID: {game_session.id}")
    print(f"Turn Number: {game_session.turn_number}")
    print(f"Winning Cards: {game_session.winning_cards}")
    print()

# Close the database connection
db.close()
