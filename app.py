#Import library
from flask import Flask, render_template, request, session, url_for, redirect,g

from hashlib import md5
import random
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
		#fetch search result
		sql = 'select distinct airline_name, flight_number, departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
		keys = (depart_airport, arrive_airport, depart_date) 
		result = fetchall(sql,keys)
		# case handling
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
	if doorman('Customer'):
		return redirect(url_for("customer"))
	if doorman('booking_agent'):
		return redirect(url_for('agent'))
	elif doorman('airline_staff'):
		return redirect(url_for('staff'))
	return render_template('login.html')

#Authenticates the login
@app.route('/loginAuth', methods=['POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form.get('username')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	usertype = request.form.get('usertype')
	agent_id = request.form.get('agent_id')

	# execute sql to check for authenticity
	#booking agent listed alone
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
		sql = 'SELECT * FROM ' + usertype + \
			' WHERE email = %s and password = %s'
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
		elif usertype == 'Booking_agent':
			return redirect(url_for('agent'))
		elif usertype == 'airline_staff':
			return redirect(url_for('staff'))
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
		if modify(sql,keys):
			register_success = 'Register succeeded, welcome.'
			return render_template('index.html',\
				 register_success = register_success)

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
		if modify(sql,keys):
			register_success = 'Register succeeded, welcome.'
			return render_template('index.html',\
				 register_success = register_success)

@app.route('/regStaffAuth', methods=['POST'])
def regStaffAuth():
	#grabs information from the forms
	email = request.form.get('email')
	password = md5(request.form.get('password').encode('utf-8')).hexdigest()
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	airline_name = request.form.get('airline_name')
	dob = request.form.get('date_of_birth')


	#check if airline exists
	sql = 'SELECT * FROM airline WHERE name = %s'
	key = (airline_name)
	data = fetchall(sql,key)
	if not data:
		error = 'The airline does not exist'
		return render_template('/registers/reg_staff.html', error = error)

	# check if the email already exists
	sql = 'SELECT * FROM airline_staff WHERE email = %s'
	key = (email)
	data = fetchone(sql, key)

	#case handling
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('/registers/reg_staff.html', error = error)
	else:
		sql = 'INSERT INTO airline_staff \
			VALUES(%s, %s, %s,%s,%s,%s)'
		keys = (email,password,first_name,last_name,dob,airline_name)
		if modify(sql,keys):
			register_success = 'Register succeeded, welcome.'
			return render_template('index.html',\
				 register_success = register_success)

@app.route('/customer',methods=['GET','POST'])
def customer():

	if not doorman('Customer'):
		return render_template('noAuth.html')

	#* get name for welcome message
	username = session.get('username')
	sql = 'select name from customer where email = %s'
	key = (username)
	name = fetchone(sql,key)
	
	#* view my flights
	sql = 'SELECT * FROM flight natural join ticket WHERE \
           	ticket.customer_email = %s and departure_time > now()'
	key = (username)
	my_flight = fetchall(sql,key)

	#* flight search
	# check for search scinario
	if request.form.get('airport_search'):
		depart_airport = request.form.get('depart_airport')
		arrive_airport = request.form.get('arrive_airport')
		depart_date = request.form.get('depart_date')
		return_date = request.form.get('return_date')
		sql = 'select distinct airline_name, flight_number, departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
		keys = (depart_airport, arrive_airport, depart_date) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No outgoing flight exists'
			return render_template('customer.html', \
				error1=error,name=name, myflight=my_flight)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
			keys = (arrive_airport, depart_airport, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('customer.html',search1=result,
					search2=return_flight,name=name, myflight=my_flight)
		return render_template('customer.html',\
			search1=result,name=name, myflight=my_flight)
	elif request.form.get('city_search'):
		depart_city = request.form.get('depart_city')
		arrive_city = request.form.get('arrive_city')
		depart_date = request.form.get('depart_date')
		return_date = request.form.get('return_date')
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
			return render_template('customer.html', \
				error2=error,name=name, myflight=my_flight)
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
		return render_template('customer.html',\
			name=name, myflight=my_flight,search1=result)

	# * purchase tickets
	# select ticket to purchase
	# TODO Add buy what you see button
	if request.form.get('purchase_search'):
		airline_name = request.form.get('airline_name')
		flight_num = request.form.get('flight_num')
		departure_datetime = request.form.get('departure_datetime')
		sql = 'select * from flight where airline_name = %s and \
				flight_number = %s and departure_time = %s'
		keys = (airline_name, flight_num, departure_datetime) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No such flight exists'
			return render_template('customer.html', \
				error3=error,name=name, myflight=my_flight)

		#calculate price
		sql = 'select count(*) as head from ticket where airline_name = %s \
			and flight_number = %s and departure_time = %s'
		key = (result[0]['airline_name'],result[0]['flight_number'],\
			result[0]['departure_time'])
		purchase_count = fetchone(sql,key)
		purchase_count = purchase_count['head']
		total_seats = fetchone('select seats from airplane where \
			airplane.id = %s',(result[0]['airplane_id']))['seats']
		result[0]['availability'] = 'YES'
		session['availability'] = 'YES'
		if purchase_count/total_seats == 1:
			result[0]['availability'] = 'NO'
			session['availability'] = 'NO'
		elif purchase_count/total_seats >= 0.7:
			result[0]['price'] = result[0]['price'] * 1.2
		# gather purchase info
		session['airline_name'] = result[0]['airline_name']
		session['flight_number'] = result[0]['flight_number']
		session['departure_time'] = result[0]['departure_time']
		session['sold_price'] = result[0]['price']
		return render_template('customer.html',\
			search3=result,name=name, myflight=my_flight)

	#actual purchase	
	if request.form.get('purchase_submit'):
		card_number = request.form.get('card_number')
		card_type = request.form.get('card_type')
		name_on_card = request.form.get('name_on_card')
		expiration_date = request.form.get('expiration_date')
		if not card_number.isdigit():
			purchase_error = 'Please enter only number in the card number box'
			return render_template('customer.html',name=name, \
				myflight=my_flight, purchase_error= purchase_error)
		if session['availability'] == 'NO':
			purchase_error = 'Flight not available, sorry.'
			return render_template('customer.html',name=name, \
				myflight=my_flight, purchase_error= purchase_error)
		sql = 'insert into ticket values \
			(%s,%s,%s,%s,%s,%s, CURDATE(), CURTIME(),%s, %s,%s,%s,NULL)'
		key = (random.randint(1,255),session['sold_price'],card_type, \
			card_number, name_on_card, expiration_date, \
				session['flight_number'], \
				session['departure_time'],session['airline_name'], \
					session['username'])
		if modify(sql,key):
			purchase_success='Purchase succeeded! Thank you for your support.'
			return render_template('customer.html', name=name,\
				myflight=my_flight,purchase_success = purchase_success)
		else:
			purchase_error = 'Purchase failed. Please try again.'
			return render_template('customer.html', name=name, \
				myflight=my_flight, purchase_error= purchase_error)

	# * give rating and comment
	if request.form.get('start_comment'):
		#fetch flight to comment
		sql = 'SELECT * FROM flight natural join ticket WHERE \
           	ticket.customer_email = %s and departure_time < now()'
		key = (username)
		flight_to_comment = fetchall(sql,key)
		return render_template('customer.html',\
			flight_to_comment=flight_to_comment,name=name, myflight=my_flight)

	if request.form.get('submit_comment'):
		#grab comment content
		airline_name = request.form.get('airline_name')
		flight_number = str(request.form.get('flight_number'))
		departure_datetime = request.form.get('departure_time')
		rating = str(request.form.get('rating'))
		comment = request.form.get('comment')

		#fetch ticket id
		sql = 'select ticket_id from ticket where airline_name = %s and \
			flight_number = %s and departure_time = %s and customer_email = %s'
		keys =(airline_name,flight_number,departure_datetime,username)
		ticket_id = fetchone(sql,keys)['ticket_id']

		#insert the comment
		sql = 'insert into comment values (%s, %s, %s)'
		key = (str(ticket_id),rating,comment)
		if modify(sql,key):
			comment_status = 'Comment successful, we appreciate your feedback'
			return render_template('customer.html', \
				name=name, myflight=my_flight,comment_status=comment_status)
		else:
			comment_status = 'Something went wrong, please try again'
			return render_template('customer.html', \
				name=name, myflight=my_flight,comment_status=comment_status)

	return render_template('customer.html', name=name, myflight=my_flight)

@app.route('/agent', methods=['GET','POST'])
def agent():

	if not doorman('Booking_agent'):
		return render_template('noAuth.html')

	#* get name for welcome message
	username = session.get('username')
	
	#* view my flights
	sql = 'SELECT * FROM flight natural join ticket WHERE  \
		ticket.booking_agent_id = (select booking_agent_id from booking_agent\
			 where email = %s) and departure_time > now()'
	key = (username)
	my_flight = fetchall(sql,key)

	#* flight search
	depart_airport = request.form.get('depart_airport')
	arrive_airport = request.form.get('arrive_airport')
	depart_date = request.form.get('depart_date')
	return_date = request.form.get('return_date')
	depart_city = request.form.get('depart_city')
	arrive_city = request.form.get('arrive_city')
	

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
			return render_template('agent.html', \
				error1=error,name=username, myflight=my_flight)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport = %s and DATE(departure_time) = %s'
			keys = (arrive_airport, depart_airport, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('agent.html',search1=result,
					search2=return_flight,name=username, myflight=my_flight)
		return render_template('agent.html',\
			search1=result,name=username, myflight=my_flight)
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
			return render_template('agent.html', \
				error2=error,name=username, myflight=my_flight)
		if return_date:
			sql = 'select distinct airline_name,flight_number,departure_time, \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport =  \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) = %s'
			keys = (arrive_city, depart_city, return_date)
			return_flight = fetchall(sql, keys)
			return render_template('agent.html',search1=result,
					search2=return_flight,name=username, myflight=my_flight)
		return render_template('agent.html',\
			name=username, myflight=my_flight,search1=result)

	# * purchase tickets
	# todo purchase 
	airline_name = request.form.get('airline_name')
	flight_num = request.form.get('flight_num')
	departure_datetime = request.form.get('departure_datetime')

	# select ticket to purchase
	# TODO Add buy what you see buttonreturn
	if airline_name:
		sql = 'select * from flight where airline_name = %s and \
				flight_number = %s and departure_time = %s'
		keys = (airline_name, flight_num, departure_datetime) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No such flight exists'
			return render_template('agent.html', \
				error3=error,name=username, myflight=my_flight)

		#calculate price
		sql = 'select count(*) as head from ticket where airline_name = %s \
			and flight_number = %s and departure_time = %s'
		key = (result[0]['airline_name'],result[0]['flight_number'],\
			result[0]['departure_time'])
		purchase_count = fetchone(sql,key)
		purchase_count = purchase_count['head']
		total_seats = fetchone('select seats from airplane where \
			airplane.id = %s',(result[0]['airplane_id']))['seats']
		result[0]['availability'] = 'YES'
		session['availability'] = 'YES'
		if purchase_count/total_seats == 1:
			result[0]['availability'] = 'NO'
			session['availability'] = 'NO'
		elif purchase_count/total_seats >= 0.7:
			result[0]['price'] = result[0]['price'] * 1.2
		# gather purchase info
		session['airline_name'] = result[0]['airline_name']
		session['flight_number'] = result[0]['flight_number']
		session['departure_time'] = result[0]['departure_time']
		session['sold_price'] = result[0]['price']
		return render_template('agent.html',\
			search3=result,name=username, myflight=my_flight)

	#actual purchase	
	if request.form.get('card_number'):
		#grab purchase info
		customer_email = request.form.get('customer_email')
		card_number = request.form.get('card_number')
		card_type = request.form.get('card_type')
		name_on_card = request.form.get('name_on_card')
		expiration_date = request.form.get('expiration_date')

		#verify card number validity
		if not card_number.isdigit():
			purchase_error = 'Please enter only number in the card number box'
			return render_template('agent.html',name=username, \
				myflight=my_flight, purchase_error= purchase_error)

		#verify customer email validity
		if not fetchone('select * from customer where email = %s',\
			(customer_email)):
			purchase_error = 'Please enter the correct customer email'
			return render_template('agent.html',name=username, \
				myflight=my_flight, purchase_error= purchase_error)

		#check flight availability
		if session['availability'] == 'NO':
			purchase_error = 'Flight not available, sorry.'
			return render_template('agent.html',name=username, \
				myflight=my_flight, purchase_error= purchase_error)

		#fetch booking agent id
		sql = 'select booking_agent_id from booking_agent where email = %s'
		keys = (username)
		booking_agent_id = fetchone(sql,keys)['booking_agent_id']

		#make sql insert
		sql = 'insert into ticket values \
			(%s,%s,%s,%s,%s,%s, CURDATE(), CURTIME(),%s, %s,%s,%s,%s)'
		key = (random.randint(1,255),session['sold_price'],card_type, \
			card_number, name_on_card, expiration_date, \
				session['flight_number'], \
				session['departure_time'],session['airline_name'], \
					customer_email, booking_agent_id)
		if modify(sql,key):
			purchase_success='Purchase succeeded! Thank you for your support.'
			return render_template('agent.html', name=username,\
				myflight=my_flight,purchase_success = purchase_success)
		else:
			purchase_error = 'Purchase failed. Please try again.'
			return render_template('agent.html', user=username, \
				myflight=my_flight, purchase_error= purchase_error)

	return render_template('agent.html', name = username, myflight = my_flight)

@app.route('/staff',methods=["GET","POST"])
def staff():
	if not doorman('airline_staff'):
		return render_template('noAuth.html')

	#* get name for welcome message
	username = session.get('username')

	#get airline name once and for all
	sql = 'select airline_name from airline_staff where email = %s'
	key = (username)
	airline_name = fetchone(sql,key)['airline_name']
	
	#* view my flights
	sql = 'SELECT * FROM flight WHERE airline_name = %s \
		and departure_time between now() and date_add(now(), interval 30 day)'
	key = (airline_name)
	my_flight = fetchall(sql,key)

	#* set future flight view
	# check for search scinario
	if request.form.get('airport_search'):
		depart_airport = request.form.get('depart_airport')
		arrive_airport = request.form.get('arrive_airport')
		start_date = request.form.get('start_date')
		end_date = request.form.get('end_date')
		sql = 'select distinct airline_name, flight_number, departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = %s and \
				arrival_airport= %s and DATE(departure_time) between %s and %s'
		keys = (depart_airport, arrive_airport, start_date,end_date) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No such flight exists'
			return render_template('staff.html', \
				error1=error,name=username, myflight=my_flight)
		return render_template('staff.html',\
			search1=result,name=username, myflight=my_flight)
	elif request.form.get('city_search'):
		depart_city = request.form.get('depart_city')
		arrive_city = request.form.get('arrive_city')
		start_date = request.form.get('start_date')
		end_date = request.form.get('end_date')
		sql = 'select distinct airline_name,flight_number,departure_time , \
				arrival_time, departure_airport, arrival_airport, \
				status  from flight where departure_airport = \
				(select name from airport where city = %s) and \
				arrival_airport = (select name from airport where city = %s) \
				and DATE(departure_time) between %s and %s'
		keys = (depart_city, arrive_city, start_date,end_date) 
		result = fetchall(sql,keys)
		if not result:
			error = 'No such flight exists'
			return render_template('staff.html', \
				error2=error,name=username, myflight=my_flight)
		return render_template('staff.html',\
			name=username, myflight=my_flight,search1=result)

	#* view customer by flight
	if request.form.get('customer_search'):
		flight_num = str(request.form.get('flight_num'))
		departure_datetime = request.form.get('depart_datetime')
		sql = 'select * from customer where email in (select distinct\
			customer_email from ticket where airline_name = %s and \
			flight_number = %s and departure_time = %s)'
		keys = (airline_name,flight_num,departure_datetime)
		result = fetchall(sql,keys)
		if not result:
			error = 'No such customer exists'
			return render_template('staff.html', \
				error3=error,name=username, myflight=my_flight)
		return render_template('staff.html',\
			name=username, myflight=my_flight,search3=result)

	# * create new flight
	if request.form.get('create_flight_submit'):
		airplane_id = str(request.form.get('airplane_id'))
		depart_airport = request.form.get('depart_airport')
		arrive_airport = request.form.get('arrive_airport')
		price = str(request.form.get('price'))
		status = request.form.get('status')
		depart_datetime = request.form.get('depart_datetime')
		arrive_datetime = request.form.get('arrive_datetime')

		#validate info
		if not fetchone('select * from airplane where id = %s',\
			(airplane_id)):
			status = 'no such airplane exists,try again'
			return render_template('staff.html', \
				name = username, myflight = my_flight, \
				create_flight_status=status)
		if not fetchone('select * from airport where %s in \
			(select name from airport) and %s in (select name from airport)',\
			(depart_airport,arrive_airport)):
			status = 'airport not correct,try again'
			return render_template('staff.html', \
				name = username, myflight = my_flight, \
				create_flight_status=status)
		#get flight number
		sql = 'select max(flight_number) as max_num from flight\
			 where airline_name = %s'
		keys = (airline_name)
		flight_num = str(fetchone(sql,keys)['max_num'] + 1)
		sql = 'insert into flight values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		keys = (flight_num,depart_datetime,arrive_datetime,price, \
			status,airline_name,airplane_id,depart_airport,arrive_airport)
		if modify(sql,keys):
			status = 'Creation success'
			return render_template('staff.html', \
				name = username, myflight = my_flight, \
				create_flight_status=status)
		else:
			status = 'Creation failed, try again'
			return render_template('staff.html', \
				name = username, myflight = my_flight, \
				create_flight_status=status)

	# * change flight status
	if request.form.get('change_status'):
		flight_num =  str(request.form.get('flight_num'))
		depart_datetime =  request.form.get('depart_datetime')
		status = request.form.get('status')

		#check flight validity
		sql = 'select * from flight where flight_number = %s and \
			departure_time = %s and airline_name = %s'
		keys = (flight_num,depart_datetime, airline_name)
		if not fetchone(sql,keys):
			change_status = 'Flight not exists, please try again'
			return render_template('staff.html', name = username, \
				myflight = my_flight, change_status = change_status)
		#make sql op
		sql = 'update flight set status = %s where flight_number = %s and \
			departure_time = %s and airline_name = %s'
		keys = (status, flight_num, depart_datetime, airline_name)
		if modify(sql,keys):
			change_status = 'Status change success'
			return render_template('staff.html', name = username, \
				myflight = my_flight, change_status = change_status)
		else:
			change_status = 'Something went wrong, please try again'
			return render_template('staff.html', name = username, \
				myflight = my_flight, change_status = change_status)
	
	#* add airplane
	if request.form.get('add_airplane'):
		seats =  str(request.form.get('seats'))
		#get the last airplane id
		sql = 'select max(id) as id_max from airplane where airline_name = %s '
		keys = (airline_name)
		max_id = fetchall(sql,keys)[0]['id_max']
		airplane_id = max_id + 1
		sql = 'insert into airplane values (%s, %s, %s)'
		keys = (str(airplane_id), seats, airline_name)
		if modify(sql,keys):
			add_airplane_status = 'Airplane add success'
			result = fetchall('select * from airplane where airline_name = %s'\
				, airline_name)
			return render_template('staff.html', name = username, \
				myflight = my_flight, add_airplane_status = \
					add_airplane_status, add_airplane = result)
		else:
			add_airplane_status = 'Something went wrong, please try again'
			return render_template('staff.html', name = username, \
				myflight = my_flight, add_airplane_status = \
					add_airplane_status)
	
	#* add airport
	if request.form.get('add_airport'):
		airport_name =  request.form.get('airport_name')
		airport_city =  request.form.get('airport_city')
		# validate airport name
		sql = 'select * from airport where name = %s '
		keys = (airport_name)
		if fetchone(sql,keys):
			add_airport_status = 'Airport already exists, try again'
			return render_template('staff.html', name = username, \
				myflight = my_flight, add_airport_status = \
					add_airport_status)
		sql = 'insert into airport values (%s, %s)'
		keys = (airport_name, airport_city)
		if modify(sql,keys):
			add_airport_status = 'Airport add success'
			return render_template('staff.html', name = username, \
				myflight = my_flight, add_airport_status = \
					add_airport_status)
		else:
			add_airport_status = 'Something went wrong, please try again'
			return render_template('staff.html', name = username, \
				myflight = my_flight, add_airport_status = \
					add_airport_status)
	
	return render_template('staff.html', name = username, myflight = my_flight)

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