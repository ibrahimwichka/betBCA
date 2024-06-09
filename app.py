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
            amount INTEGER NOT NULL,
            vote INTEGER,
            status TEXT DEFAULT "Active",
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
        ("Philadelphia Eagles vs. Kansas City Chiefs 🏈\n(06/19/2024)", "Eagles", "Chiefs", +200, -300, "Bet Ongoing!"),
        ("Golden State Warriors vs. Boston Celtics 🏀\n(06/20/2024)", "Warriors", "Celtics", -800, +200, "Bet Ongoing!")
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
            session['user_id'] = user['id']
            return redirect('/your_bets')
        else:
            error = 'Invalid username or password.'
            return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/your_bets')
def your_bets():
    if 'username' in session:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']

        cursor.execute('''
            SELECT ub.user_bet_id, ub.amount, ub.vote, b.bet_id, b.bet_topic, b.choice1, b.choice2, b.odds1, b.odds2, b.result
            FROM user_bets ub
            JOIN bets b ON ub.bet_id = b.bet_id
            WHERE ub.user_id = ?
        ''', (session['user_id'],))

        user_bets = cursor.fetchall()
        db.close()
        
        return render_template('your_bets.html', logged_in=True, username=session['username'], user_points = user_points, user_bets= user_bets)
    else:
        return render_template('your_bets.html')

@app.route('/all_bets')
def all_bets():
    if 'username' in session:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            '''SELECT * FROM bets LIMIT 2'''
        )
        rows = cursor.fetchall()
        bet_ids = [row['bet_id'] for row in rows]
        bet_topics = [row['bet_topic'] for row in rows]
        choices_1 = [row['choice1'] for row in rows]
        choices_2 = [row['choice2'] for row in rows]
        odds_1 = [row['odds1'] for row in rows]
        odds_2 = [row['odds2'] for row in rows]
        results = [row['result'] for row in rows]

        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']
        
        db.close()
        return render_template(
            'all_bets.html', 
            logged_in=True, 
            username=session['username'], user_points=user_points,
            bet_ids = bet_ids, bet_topics = bet_topics, choices_1 = choices_1, choices_2 = choices_2, odds_1 = odds_1, odds_2 = odds_2, results = results
        )
    else:
        return render_template('all_bets.html')

@app.route('/submit_bet', methods=['POST'])
def submit_bet():
    if 'username' in session:
        bet_id = int(request.form['bet_id'])
        choice = request.form['team']
        amount = int(request.form['amount'])
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']

        if (amount > user_points):
            return redirect('/all_bets')

        cursor.execute('UPDATE users SET points = ? WHERE username = ?', (user_points-amount, session['username']))
        db.commit()

        cursor.execute('INSERT INTO user_bets (user_id, bet_id, amount, vote) VALUES (?, ?, ?, ?)',
                       (session['user_id'], bet_id, amount, choice))
        db.commit()
        db.close()

        return redirect('/your_bets')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
