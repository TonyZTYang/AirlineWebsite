CREATE TABLE airline(
	name varchar(255) PRIMARY KEY
);

CREATE TABLE airplane(
	id int(255),
	seats int(255),
	airline_name varchar(255),
	PRIMARY KEY (id, airline_name),
	FOREIGN KEY (airline_name) REFERENCES airline(name) ON DELETE CASCADE
);

CREATE TABLE airline_staff(
	username varchar(255) PRIMARY KEY,
	password varchar(255),
	first_name varchar(255),
	last_name varchar(255),
	date_of_birth date,
	airline_name varchar(255),
	FOREIGN KEY (airline_name) REFERENCES airline(name) ON DELETE CASCADE
);

CREATE TABLE phone_num (
	phone_number bigint(20) PRIMARY KEY,
	owner varchar(255),
	FOREIGN KEY (owner) REFERENCES airline_staff(username) ON DELETE CASCADE
);

CREATE TABLE airport(
	name varchar(255) PRIMARY KEY,
	city varchar(255)
);

CREATE TABLE flight(
	flight_number int(255),
	departure_time datetime,
	arrival_time datetime,
	price float,
	status varchar(20),
	airline_name varchar(255),
	airplane_id int(255),
	departure_airport varchar(255),
	arrival_airport varchar(255),
	PRIMARY KEY (airline_name, flight_number, departure_time),
	FOREIGN KEY (airline_name, airplane_id) REFERENCES airplane(airline_name, id) ON DELETE CASCADE,
	FOREIGN KEY (departure_airport) REFERENCES airport(name) ON DELETE CASCADE,
	FOREIGN KEY (arrival_airport) REFERENCES airport(name) ON DELETE CASCADE
);

CREATE TABLE customer(
	email varchar(255) PRIMARY KEY,
	name varchar(255),
	password varchar(255),
	building_num int(255),
	street varchar(255),
	city varchar(255),
	state varchar(255),
	phone_num bigint(20),
	passport_num varchar(255),
	passort_expiration date,
	passport_country varchar(255),
	date_of_birth date
);

CREATE TABLE booking_agent(
	email varchar(255) PRIMARY KEY,
	password varchar(255),
	booking_agent_id int(255) UNIQUE
);

CREATE TABLE ticket(
	ticket_id int(255) PRIMARY KEY,
	sold_price float,
	card_type varchar(255),
	card_number bigint(20),
	name_on_card varchar(255),
	expiration_date date,
	purchase_date date,
	purchase_time time,
	flight_number int(255),
	departure_time datetime,
	airline_name varchar(255),
	customer_email varchar(255),
	booking_agent_id int(255),
	FOREIGN KEY (airline_name, flight_number, departure_time) REFERENCES flight(airline_name, flight_number, departure_time) ON DELETE CASCADE,
	FOREIGN KEY (customer_email) REFERENCES customer(email) ON DELETE CASCADE,
	FOREIGN KEY (booking_agent_id) REFERENCES booking_agent(booking_agent_id) ON DELETE CASCADE
);

CREATE TABLE comment(
	ticket_id int(255) PRIMARY KEY,
	comment varchar (255),
	FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id) ON DELETE CASCADE
);