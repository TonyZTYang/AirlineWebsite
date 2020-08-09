"""a module containing the secret key and database connection specification
"""
import pymysql.cursors

secret_key = 'Some secret key no one should know'

# Configure MySQL
db = pymysql.connect(host='mysql server address',
                     user='username',
                     password='password',
                     db='airline',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
