import os
from flask import Flask, render_template, request, redirect, session
from flask_material import Material
import sqlite3

app = Flask(__name__)
Material(app)

app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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
            points INTEGER DEFAULT 20
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bets (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bet_topic TEXT NOT NULL,
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
            amount DECIMAL(10,2) NOT NULL,
            vote INTEGER,
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
        INSERT INTO users (username, password)
        VALUES ('ibrahimwichka', 'ibrahim122'), ('bigboynate', 'naty'), ('soomark', 'markyoon')
    ''')
    cursor.execute('''
        INSERT INTO bets('bet_topic', 'choice1', 'choice2', 'odds1', 'odds2', 'result')
        VALUES 
        ("Philadelphia Eagles vs. Kansas City Chiefs", "Eagles", "Chiefs", +200, -300, ""),
        ("Golden State Warriors vs. Bostin Celtic", "Warriors", "Celtics", -800, +200, "")
    ''')
    db.commit()
    db.close()

drop_all_tables()
create_tables()
insert_data()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('your_bets.html', logged_in=True, username=session['username'])
    else:
        return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        db.close()
        if user and password == user['password']:
            session['username'] = username
            return redirect('/your_bets')
        else:
            error = 'Invalid username or password.'
            return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/your_bets')
def your_bets():
    if 'username' in session:
        return render_template('your_bets.html', logged_in=True, username=session['username'])
    else:
        return render_template('your_bets.html')

@app.route('/all_bets')
def all_bets():
    if 'username' in session:
        return render_template('all_bets.html', logged_in=True, username=session['username'])
    else:
        return render_template('all_bets.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
