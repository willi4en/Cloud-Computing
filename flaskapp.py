import sqlite3
import os
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
	try:
		connection = sqlite3.connect('/home/ubuntu/flaskapp/database.db')
	except Exception as e:
		print("Oof", e)
		if connection:
			connection.close()
	return connection

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		conn = get_db_connection()
		cur = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		if username is None or password is None:
			return render_template('login.html', error="Please make sure all fields are filled out.")
		cur.execute("SELECT * from users where username = (?) AND password = (?)", [username, password])
		user = cur.fetchone()
		if (user is not None):
			conn.close()
			session['currentUser'] = user[0]
			return redirect(url_for('profile'))
		else:
			userList = ""
			cur.execute("SELECT * FROM users")
			for row in cur:
				userList = userList + "{}, {}, {}, {}, {}, {}, {}\n".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
			conn.close()
			return render_template('login.html', error=userList)
	elif request.method == 'GET':
		return render_template('login.html')


@app.route('/account_creation', methods=['GET', 'POST'])
def createAccount():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		email = request.form['email']
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("INSERT INTO users (username, password, firstName, lastName, email) VALUES (?,?,?,?,?)", [username, password, firstName, lastName, email])
		conn.commit()
		conn.close()
		return redirect(url_for('home'))
	elif request.method == 'GET':
		return render_template('createAccount.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
	if request.method == 'POST':
		return redirect(url_for('home'))
	else:
		currentUser = session['currentUser']
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE id = (?)", [currentUser])
		user = cur.fetchone()
		conn.close()
		if (user is None):
			return redirect(url_for('home'))
		else:
			return render_template('profile.html', username=user[2], firstName=user[4], lastName=user[5], email=user[6])


if __name__ == '__main__':
	app.run()
