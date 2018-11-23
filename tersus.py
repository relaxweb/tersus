from flask import Flask, session, redirect, url_for, escape, request, render_template

import pymysql
db = pymysql.connect("localhost", "root", "relaxwebpass108", "tersus")

app = Flask(__name__, static_url_path='/static')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# INDEX PAGE
@app.route('/')
def index():
    # if 'username' in session:
    cursor = db.cursor()
    sql = "SELECT * FROM user_login"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('dashboard.html', results=results)
        # return 'Logged in as %s' % escape(session['username'])
    # return redirect(url_for('login'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html', name='name')

# LOGOUT
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))