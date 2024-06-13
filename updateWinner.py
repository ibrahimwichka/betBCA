import sqlite3
import flask

from app import get_db_connection


db = get_db_connection()
cursor = db.cursor()
cursor.execute('''UPDATE bets SET result = "Eagles" WHERE bet_id = 1''')
cursor.execute('''UPDATE bets SET result = "Warriors" WHERE bet_id = 2''')
db.commit()
db.close()
