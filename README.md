# Airline Website: Bootstrap + Vue + Flask + Mysql
A database system for a hypothetic airline company as the final project for CSCI-SHU 213 Databases.

## Usage
1. Download the whole project.
2. Install requirements using the following code with terminal in the project folder.

    $ pip3 install -r -U requirement.txt

3. Install mysql, create a database with name 'airline' and run sql files under 'sql' folder for table creation and data insertion.
4. Go to app.py, comment out line 3: 'from config import db, secret_key'.
5. Uncomment the block of comment starting with 'replacement of config.py', and change the secret key and databse setting.
6. Run app.py
7. In browser open http://localhost:5000 to use the app.
