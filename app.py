#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from config import db, secret_key
from util import fetchall

'''
# replacement of config.py
import pymysql.cursors

secret_key = 'Some secret key no one should know'

#Configure MySQL
db = pymysql.connect(host='mysql server address',
                       user='username',
                       password='password',
                       db= 'airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
'''

#Initialize the app from Flask
app = Flask(__name__)

#Define a route to index
@app.route('/', methods = ['GET'])
def index_get():
	return render_template('index.html')

#Add route for public info search
@app.route('/', methods = ['POST'])
def public_info_search():
	# fetch info from form
	depart_airport = request.form.get('depart_airport')
	arrive_airport = request.form.get('arrive_airport')
	depart_date = request.form.get('depart_date')
	return_date = request.form.get('return_date')
	depart_city = request.form.get('depart_city')
	arrive_city = request.form.get('arrive_city')
	airline_name = request.form.get('airline_name')
	flight_num = request.form.get('flight_num')

	# check for search scinario
	if depart_airport:
		sql = 'select distinct airline_name, flight_number, departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
		keys = (depart_airport, arrive_airport, depart_date) 
		result = fetchall(sql,keys)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
			keys = (arrive_airport, depart_airport, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('index.html',search1=result,
					search2=return_flight)
		return render_template('index.html',search1=result)
	elif depart_city:
		sql = 'select distinct airline_name,flight_number,departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) = %s'
		keys = (depart_city, arrive_city, depart_date) 
		result = fetchall(sql,keys)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport =  \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) = %s'
			keys = (arrive_city, depart_city, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('index.html',search1=result,
					search2=return_flight)
		return render_template('index.html',search1=result)
	elif airline_name:
		sql = 'select distinct airline_name,flight_number,departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where airline_name = %s and \
				flight_number = %s \
				and DATE(departure_time) = %s'
		keys = (airline_name, flight_num, depart_date) 
		result = fetchall(sql,keys)
		return render_template('index.html',search3=result)
	else:
		return 'form submission not matching'

#Define route for login type choosing
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register type choosing
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = db.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = db.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		db.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
    
    username = session['username']
    cursor = db.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = db.cursor()
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	db.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = secret_key

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
