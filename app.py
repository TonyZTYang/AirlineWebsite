#Import library
from flask import Flask, render_template, request, session, url_for, redirect
from hashlib import md5
# import module
from config import db, secret_key
from util import fetchall, fetchone, modify, doorman

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
	error = None
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
		if not result:
			error = 'No outgoing flight exists'
			return render_template('index.html', error1=error)
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
		if not result:
			error = 'No outgoing flight exists'
			return render_template('index.html', error2=error)
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
		if not result:
			error = 'No such flight exists'
			return render_template('index.html', error3=error)
		return render_template('index.html',search3=result)
	

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Authenticates the login
@app.route('/loginAuth', methods=[ 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form.get('username')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	usertype = request.form.get('usertype')
	agent_id = request.form.get('agent_id')

	# execute sql to check for authenticity
	if usertype == 'Booking_agent':
			if agent_id:
				sql = 'SELECT * FROM ' + usertype + ' WHERE email = %s \
				and password = %s and booking_agent_id = %s'
				keys = (username, password, agent_id)
				data = fetchone(sql,keys)
			else:
				error = 'Booking agent id not entered'
				return render_template('login.html', error=error)
	else:
		sql = 'SELECT * FROM ' + usertype + ' WHERE email = %s and password = %s'
		keys = (username, password)
	data = fetchone(sql,keys)

	# case handling
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['usertype'] = usertype
		if usertype == 'Customer':
			return redirect(url_for('customer'))
		# return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Define routes for register types
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/register/customer')
def reg_customer():
	return render_template('/registers/reg_customer.html')

@app.route('/register/agent')
def reg_agent():
	return render_template('/registers/reg_agent.html')

@app.route('/register/staff')
def reg_staff():
	return render_template('/registers/reg_staff.html')

#Authenticates the register
@app.route('/regCustomerAuth', methods=['POST'])
def regCustomerAuth():
	#grabs information from the forms
	email = request.form.get('email')
	name = request.form.get('name')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	building_num = request.form.get('building_number')
	street = request.form.get('street')
	city = request.form.get('city')
	state = request.form.get('state')
	phone_num = request.form.get('phone_number')
	passport_num = request.form.get('passport_number')
	passport_expiration = request.form.get('passport_expiration')
	passport_country = request.form.get('passport_country')
	dob = request.form.get('date_of_birth')

	# info validation
	if not building_num.isdigit() and not phone_num.isdigit():
		error = 'Please enter in correct form'
		return render_template('/registers/reg_customer.html', error = error)

	# check if the email already exists
	sql = 'SELECT * FROM Customer WHERE email = %s'
	key = (email)
	data = fetchone(sql, key)

	#case handling
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('/registers/reg_customer.html', error = error)
	else:
		sql = 'INSERT INTO Customer \
			VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		keys = (email,name,password,building_num,street,city,state,phone_num,
		passport_num, passport_expiration, passport_country, dob)
		modify(sql,keys)
		return render_template('index.html')

@app.route('/regAgentAuth', methods=['POST'])
def regAgentAuth():
	#grabs information from the forms
	email = request.form.get('email')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	agent_id = request.form.get('agent_id')

	# info validation
	if not agent_id.isdigit() :
		error = 'Please enter in correct form'
		return render_template('/registers/reg_agent.html', error = error)

	# check if the email already exists
	sql = 'SELECT * FROM Booking_agent WHERE email = %s'
	key = (email)
	data = fetchone(sql, key)

	#case handling
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('/registers/reg_agent.html', error = error)
	else:
		sql = 'INSERT INTO Booking_agent \
			VALUES(%s, %s, %s)'
		keys = (email,password,agent_id)
		modify(sql,keys)
		return render_template('index.html')

@app.route('/regStaffAuth', methods=['POST'])
def regStaffAuth():
	#grabs information from the forms
	email = request.form.get('email')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	airline_name = request.form.get('airline_name')
	dob = request.form.get('date_of_birth')

	# check if the email already exists
	sql = 'SELECT * FROM airline_staff WHERE email = %s'
	key = (email)
	data = fetchone(sql, key)

	#check if airline exists
	sql = 'SELECT * FROM airline WHERE name = %s'
	key = (airline_name)
	data = fetchall(sql,key)
	if not data:
		error = 'The airline does not exist'
		return render_template('/registers/reg_staff.html', error = error)

	#case handling
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('/registers/reg_staff.html', error = error)
	else:
		sql = 'INSERT INTO airline_staff \
			VALUES(%s, %s, %s,%s,%s,%s)'
		keys = (email,password,first_name,last_name,dob,airline_name)
		modify(sql,keys)
		return render_template('index.html')

@app.route('/customer',methods=['GET','POST'])
def customer():
	if not doorman('Customer'):
		return render_template('noAuth.html')

	#get name for welcome message
	username = session.get('username')
	sql = 'select name from customer where email = %s'
	key = (username)
	name = fetchone(sql,key)
	
	#view my flights
	sql = 'SELECT * FROM flight natural join ticket WHERE \
           	ticket.customer_email = %s and departure_time > now()'
	key = (username)
	my_flight = fetchall(sql,key)

	#flight search
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
		if not result:
			error = 'No outgoing flight exists'
			return render_template('customer.html', error1=error,name=name, myflight=my_flight)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
			keys = (arrive_airport, depart_airport, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('customer.html',search1=result,
					search2=return_flight,name=name, myflight=my_flight)
		return render_template('customer.html',search1=result,name=name, myflight=my_flight)
	elif depart_city:
		sql = 'select distinct airline_name,flight_number,departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) = %s'
		keys = (depart_city, arrive_city, depart_date) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No outgoing flight exists'
			return render_template('customer.html', error2=error,name=name, myflight=my_flight)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport =  \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) = %s'
			keys = (arrive_city, depart_city, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('customer.html',search1=result,
					search2=return_flight,name=name, myflight=my_flight)
		return render_template('customer.html',name=name, myflight=my_flight,search1=result)


	return render_template('customer.html', name=name, myflight=my_flight)
		


@app.route('/logout')

def logout():
	session.pop('username',None)
	session.pop('usertype', None)
	return redirect('/')

app.secret_key = secret_key

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
