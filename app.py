import os
from flask import Flask, render_template, request, redirect, session
from jinja2 import Environment
from flask_material import Material
import sqlite3
# from cryptography.fernet import Fernet
# import base64

app = Flask(__name__)
Material(app)

app.jinja_env.globals.update(zip=zip)

app.secret_key = os.urandom(24)
# key = base64.urlsafe_b64encode(os.urandom(32))
# cipher_suite = Fernet(key)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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
        if user and password == (user['password']):
            print(username + " signed in!")
            session['username'] = username
            session['user_id'] = user['id']
            return redirect('/your_bets')
        else:
            error = 'Invalid username or password.'
            return render_template('index.html', error=error)

    return redirect('/')

@app.route('/submit_sign_up', methods=['GET', 'POST'])
def submit_sign_up():
    if request.method == 'POST':
        username = request.form['username2']
        password = request.form['password2']
        dob = request.form['dob']
        sec_question = request.form['sec_question']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, DOB, security_q)
            VALUES (?, ?, ?, ?)''', (username, password , dob, sec_question)
        )
        db.commit()
        db.close()
        return redirect('/')

@app.route('/submit_pw_change', methods=['GET', 'POST'])
def submit_pw_change():
    if request.method == 'POST':
        username3 = request.form['username3']
        sec_question = request.form['sec_question2']
        new_pw = request.form["new_pw"]


        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('''SELECT username, security_q from users where username = ?''', (username3,))
        check_sec = cursor.fetchone()['security_q']
        print(check_sec)
        if (check_sec == sec_question):
            cursor.execute('''
            UPDATE users SET password = ? WHERE username = ?''', (new_pw, username3,)
            )
            db.commit()
            db.close()
            return redirect('/')
        return redirect('/forgot_pw')
        
@app.route('/your_bets')
def your_bets():
    # print(session['username'])
    if 'username' in session:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']


        cursor.execute('''
            SELECT ub.user_bet_id, ub.amount, ub.vote, b.bet_id, b.bet_topic, b.choice1, b.choice2, b.odds1, b.odds2, b.result
            FROM user_bets ub
            JOIN bets b ON ub.bet_id = b.bet_id
            WHERE ub.user_id = ? and b.result = "Bet Ongoing!"
        ''', (session['user_id'],))
        user_bets = cursor.fetchall()

        cursor.execute('''
            SELECT ub.user_bet_id, ub.amount, ub.vote, ub.status, ub.earned, b.bet_id, b.bet_topic, b.choice1, b.choice2, b.odds1, b.odds2, b.result
            FROM user_bets ub
            JOIN bets b ON ub.bet_id = b.bet_id
            WHERE ub.user_id = ? and b.result != "Bet Ongoing!"
        ''', (session['user_id'],))
        user_bets2 = cursor.fetchall()

        earned_a = 0
        for bet in user_bets2:
            if (bet['status'] == "Active"):
                if (bet['result'] == bet['vote']):
                    print(bet['result'])
                    print(bet['amount'])
                    print(bet['odds1'])
                    if (bet['result'] == bet['choice1']):
                        if (bet['odds1'] > 0):
                            earned_a = bet['amount'] + (bet['amount']/100) * bet['odds1']
                        else:
                            earned_a =  bet['amount'] + (bet['amount']/abs(bet['odds1'])) * 100
                    else:
                        if (bet['odds2'] > 0):
                            earned_a =  bet['amount'] + (bet['amount']/100) * bet['odds2']
                        else:
                            earned_a = bet['amount'] + (bet['amount']/ abs(bet['odds2'])) * 100
                    earned_a = round(earned_a, 2)
                    cursor.execute('UPDATE user_bets SET earned = ? WHERE user_bet_id = ?', (earned_a, bet['user_bet_id']))
        
        cursor.execute('''
            SELECT ub.user_bet_id, ub.amount, ub.vote, ub.status, ub.earned, b.bet_id, b.bet_topic, b.choice1, b.choice2, b.odds1, b.odds2, b.result
            FROM user_bets ub
            JOIN bets b ON ub.bet_id = b.bet_id
            WHERE ub.user_id = ? and b.result != "Bet Ongoing!"
        ''', (session['user_id'],))
        user_bets2 = cursor.fetchall()

        user_bets2_leaderboards = []
        for bet in user_bets2:
            cursor.execute(
                '''SELECT username, user_bets.earned 
                FROM users JOIN user_bets ON users.id = user_bets.user_id 
                WHERE user_bets.bet_id = ? 
                ORDER BY user_bets.earned DESC
                LIMIT 5'''
                , (bet['bet_id'],)
            )
            leaderboard_bet = cursor.fetchall()
            user_bets2_leaderboards.append(leaderboard_bet)
            
        
        if (user_points < 100):
            level = "Beginner Level 😬"
        elif (user_points <=200):
            level = "Pretty good guesser 🤓"
        elif (user_points <= 400):
            level = "A fire better 🔥 🔥"
        elif (user_points <= 700):
            level = "Elite Level 💎"
        else:
            level = "Legendary 🦄"
        db.commit()
        db.close()
       
        return render_template('your_bets.html', logged_in=True, username=session['username'], user_points = round(user_points,2) , level = level, user_bets= user_bets, user_bets2 = user_bets2, user_bets2_leaderboards = user_bets2_leaderboards)
    else:
        print("it happened")
        return redirect('/')

@app.route('/all_bets')
def all_bets():
    if 'username' in session:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            '''SELECT * FROM bets WHERE result == "Bet Ongoing!"'''
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
        if (user_points < 100):
            level = "Beginner Level 😬"
        elif (user_points <=200):
            level = "Pretty good guesser 🤓"
        elif (user_points <= 400):
            level = "A fire better 🔥 🔥"
        elif (user_points <= 700):
            level = "Elite Level 💎"
        else:
            level = "Legendary 🦄"

        db.close()
        return render_template(
            'all_bets.html', 
            logged_in=True, 
            username=session['username'], user_points= round(user_points, 2), level = level,
            bet_ids = bet_ids, bet_topics = bet_topics, choices_1 = choices_1, choices_2 = choices_2, odds_1 = odds_1, odds_2 = odds_2, results = results
        )
    else:
        print("Happened")
        return redirect('/')

@app.route('/submit_bet', methods=['POST'])
def submit_bet():
    if 'username' in session:
        bet_id_given = int(request.form['bet_id'])
        choice = request.form['team']
        amount = int(request.form['amount'])
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']

        if (amount > user_points):
            db.close()
            return redirect('/all_bets')
        
        cursor.execute('''SELECT choice1, choice2 FROM bets WHERE bet_id = ?''', (bet_id_given,))
        choices = cursor.fetchone()
        if (choice == "choice1"):
            choice = choices['choice1']
        elif (choice == "choice2"):
            choice = choices['choice2']

        cursor.execute('UPDATE users SET points = ? WHERE username = ?', (user_points-amount, session['username']))
        db.commit()

        cursor.execute('INSERT INTO user_bets (user_id, bet_id, amount, vote) VALUES (?, ?, ?, ?)',
                       (session['user_id'], bet_id_given, amount, choice))
        db.commit()
        db.close()

        return redirect('/your_bets')
    else:
        return redirect('/')

@app.route('/get_reward', methods=['POST'])
def get_reward():
    if 'username' in session:
        user_bet_id_get = request.form['user_bet_id']
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('''SELECT earned FROM user_bets where user_bet_id = ?''', (user_bet_id_get,))
        amount = cursor.fetchone()['earned']

        cursor.execute('''SELECT points FROM users WHERE username = ?''', (session['username'],))
        user_points = cursor.fetchone()['points']

        cursor.execute('UPDATE users SET points = ? WHERE username = ?', (round(user_points+amount, 2), session['username']))
        cursor.execute('UPDATE user_bets SET status = "redeemed" WHERE user_bet_id = ?', (user_bet_id_get,))

        db.commit()
        db.close()
        return redirect('your_bets')


    else:
        return redirect('/')


@app.route('/leaderboard')
def leaderboard():
    if 'username' in session:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users ORDER BY points DESC')
        leaderboard_data = cursor.fetchall()

        cursor.execute('SELECT points FROM users WHERE username = ?', (session['username'],))
        user_points = cursor.fetchone()['points']
        db.close()

        return render_template(
            'leaderboard.html', 
            logged_in=True, 
            username=session['username'],
            user_points=user_points,
            leaderboard=leaderboard_data,
            current_user=session['user_id']
        )
    else:
        return redirect('/')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template(
            'profile.html', 
            logged_in=True, 
            username=session['username']
        )
    else:
        return redirect('/')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/forgot_pw')
def forgot_pw():
    return render_template("forgot_pw.html")


if __name__ == '__main__':
    app.run(debug=True)





