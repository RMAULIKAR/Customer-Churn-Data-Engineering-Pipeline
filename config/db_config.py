import mysql.connector

def get_connection(database=None):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="use_password",
        database=database
    )

    return conn