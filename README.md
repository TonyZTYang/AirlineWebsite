# Air Ticket Reservation System 
A python database system for a hypothetic airline company as the final project for CSCI-SHU 213 Databases.


## Installation
1. Download the whole project.
2. Install requirements using the following code with terminal in the project folder.
```
$ pip3 install -r requirement.txt -U
```
3. Install mysql, create a database with name 'airline' and run sql files under 'sql' folder for table creation and data insertion.
4. Go to app.py, comment out line 3: 'from config import db, secret_key'.
5. Uncomment the block of comment starting with 'replacement of config.py', and change the secret key and databse setting.
6. Run app.py
7. In browser open http://localhost:5000 to use the app.

## Use Cases
### General
- [x] View Public Info
- [x] Register
  - [x] Customer
  - [x] Booking Agent
  - [x] Airline Staff

- [x] Login
  - [x] Customer
  - [x] Booking Agent
  - [x] Airline Staff
### Customer
- [x] View my flight
- [x] Search for flight
- [x] Purchase Tickets
- [x] Giver ratings and comments on previous flight
- [ ] Track my spending
- [x] Logout
### Booking Agent
- [x] View my flights
- [x] Search for flights
- [x] Purchase tickets
- [ ] View my commission
- [ ] View top customers
- [x] Logout
### Airline Staff
- [x] View flights
- [x] Create new flights
- [x] Change status of flights
- [x] Add airplane in the system
- [x] Add new airport in the system
- [x] View flight ratings
- [x] Add/delete phone number
- [ ] View all the booking agents
- [ ] View frequent customers
- [ ] View reports
- [ ] Comparison of revenue earned
- [ ] View top destination
- [x] Logout
### Enforcing complex constraints
- [x] Prevention of http attacks
- [x] Sessions for each user and authentications each step after login
- [x] Prepared statements
- [x] Prevent cross-site scripting

## Documentation
For full documentation (ER diagram, relational diagram and all use cases), look under [documentation folder](/documentation).
