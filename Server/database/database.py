import mysql.connector as con
from mysql.connector import errorcode
import dotenv

def delete_database():
    conf = dotenv.dotenv_values("/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB")
    db = con.connect(host='localhost', user=conf["MYSQL_USERNAME"], passwd=conf["MYSQL_PASSWORD"])
    db.cursor().execute("DROP DATABASE DatasetGenerator")

def load_database(): 
    try:
        conf = dotenv.dotenv_values("/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.envDDBB")
        db=con.connect(host="localhost", user=conf["MYSQL_USERNAME"], password=conf["MYSQL_PASSWORD"], database="DatasetGenerator")
    except con.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            db = con.connect(host='localhost', user=conf["MYSQL_USERNAME"], passwd=conf["MYSQL_PASSWORD"])
            db.cursor().execute("CREATE DATABASE DatasetGenerator")
            db.close()
            db=con.connect(host="localhost", user=conf["MYSQL_USERNAME"], password=conf["MYSQL_PASSWORD"], database="DatasetGenerator")
            db.cursor().execute("CREATE TABLE Users (mail VARCHAR(50) PRIMARY KEY, name VARCHAR(50), password VARCHAR(50))")
    return db

def insert_user(mail, name, password):
    db = load_database()
    mycursor = db.cursor()
    try:
        mycursor.execute("INSERT INTO Users (mail, name, password) VALUES (%s,%s,%s)", (mail, name, password))
        db.commit()
        print("User registered successfully!")
    except con.Error as err:
        print("The data that you entered could not be registered. Check the error above for further information!")
        print(err)
    db.close()

def get_user(mail):
    db = load_database()
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT password FROM Users WHERE mail = %s", (mail, ))
        result = mycursor.fetchone()
        db.close()
        return result[0]
    except con.Error as err:
        print("The data that you entered could not be registered. Check the error above for further information!")
        print(err)
        db.close()
        return None

def user_exists(mail):
    db = load_database()
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT mail FROM Users WHERE mail = %s", (mail, ))
        result = mycursor.fetchone()
        db.close()
        return result[0] == mail
    except:
        return False

def get_password(mail):
    db = load_database()
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT password FROM Users WHERE mail = %s", (mail, ))
        result = mycursor.fetchone()
        db.close()
        return result[0]
    except con.Error as err:
        print("The data that you entered could not be registered. Check the error above for further information!")
        print(err)
        db.close()
        return None

def print_users():
    db = load_database()
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM Users")
    result = mycursor.fetchall()
    for x in result:
        print(x)
    db.close()
    