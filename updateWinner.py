import sqlite3
import flask

from app import get_db_connection


db = get_db_connection()
cursor = db.cursor()
cursor.execute('''UPDATE bets SET result = "Chiefs" WHERE bet_id = 1''')
db.commit()
db.close()
