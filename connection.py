import mysql.connector
from mysql.connector import Error

db = "fitness_center"
user = "root"
password = "Potato828"
host = "localhost"


# connecting to database & storing the data
def connection():
    try:
        conn = mysql.connector.connect(
            database = db,
            user = user,
            password = password,
            host = host
        )

       
        if conn.is_connected():
            print("Success!")
            return conn

     # if connection fails
    except Error as e:
        print(f"Error: {e}")
        return None

# connection() --- running successfully