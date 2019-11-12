# Air Ticket Reservation System Bootstrap + Vue + Flask + Mysql
A database system for a hypothetic airline company as the final project for CSCI-SHU 213 Databases.
* Frontend: Vue + Axios
* Backend: Flask + Mysql

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
- [ ] View Public Info
- [ ] Register
  - [ ] Customer
  - [ ] Booking Agent
  - [ ] Airline Staff

- [ ] Login
  - [ ] Customer
  - [ ] Booking Agent
  - [ ] Airline Staff
### Customer
- [ ] View my flight
- [ ] Search for flight
- [ ] Purchase Tickets
- [ ] Giver ratings and comments on previous flight
- [ ] Track my spending
- [ ] Logout
### Booking Agent
- [ ] View my flights
- [ ] Search for flights
- [ ] Purchase tickets
- [ ] View my commision
- [ ] View top customers
- [ ] Logout
### Airline Staff
- [ ] View flights
- [ ] Create new flights
- [ ] Change status of flights
- [ ] Add airplane in the system
- [ ] Add new airport in the system
- [ ] View flight ratings
- [ ] View all the booking agents
- [ ] View frequent customers
- [ ] View reports
- [ ] Comparison of revenue earned
- [ ] View top destination
- [ ] Logout
### Enforcing complex constraints
- [ ] Prevention of http attacks
- [ ] Sessions for each user and authentications each step after login
- [ ] Prepared statements
- [ ] Prevent cross-site scripting

## Documentation
For full documentation (ER diagram, relational diagram and all use cases), look under [documentation folder](/documentation).
