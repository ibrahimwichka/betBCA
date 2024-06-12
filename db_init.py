import sqlite3
import flask
from app import get_db_connection

def drop_all_tables():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('PRAGMA foreign_keys = OFF;') 
    cursor.execute('DROP TABLE IF EXISTS user_bets;')
    cursor.execute('DROP TABLE IF EXISTS bets;')
    cursor.execute('DROP TABLE IF EXISTS users;')
    cursor.execute('PRAGMA foreign_keys = ON;')
    db.commit()
    db.close()

def create_tables():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            DOB TEXT,
            security_q TEXT,
            points REAL DEFAULT 20.00
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bets (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bet_topic TEXT NOT NULL,
            bet_category TEXT,
            choice1 TEXT,
            choice2 TEXT,
            odds1 INTEGER,
            odds2 INTEGER,
            result TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_bets (
            user_bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bet_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            vote INTEGER,
            status TEXT DEFAULT "Active",
            earned REAL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (bet_id) REFERENCES bets(bet_id)
        )
    ''')

    db.commit()
    db.close()

def insert_data():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, DOB, security_q)
        VALUES ('ibrahimwichka', 'ibrahim122', '12/13/2006', 'Denver'), ('bigboynate', 'naty', '4/12/2007', 'New York'), ('soomark', 'markyoon', '10/11/2007', 'New York')
    ''')
    cursor.execute('''
        INSERT INTO bets('bet_topic', 'choice1', 'choice2', 'odds1', 'odds2', 'result')
        VALUES 
        ("Philadelphia Eagles vs. Kansas City Chiefs 🏈\n(06/19/2024)", "Eagles", "Chiefs", +200, -300, "Bet Ongoing!"),
        ("Golden State Warriors vs. Boston Celtics 🏀\n(06/20/2024)", "Warriors", "Celtics", -800, +200, "Bet Ongoing!"),
        ("Chile vs. Argentina ⚽\n(06/21/2024)", "Chile", "Argentina", +600, -500, "Bet Ongoing!"),
        ("Will Ibrahim get a buzzcut over the summer? 🧑‍🦲", "Yes", "No", -500, +700, "Bet Ongoing!"),
        ("Will Soo Young & Ibrahim cross 300 touchdowns in Lunch Football before high school ends? 🏈", "Yes", "No", -800, +200, "Bet Ongoing!"),
        ("Will Yellow Win Tug of War on Field Day?", "Yes", "No", -100, +130, "Bet Ongoing!")
    ''')
    db.commit()
    db.close()

drop_all_tables()
create_tables()
insert_data()
