import psycopg2
import os

conn = psycopg2.connect('postgresql://profy:TRscICM9vdVHM9D-U9M1xw@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/profydatabase?sslmode=verify-full&options=--cluster%3Dbeige-cuscus-6334')
mycursor = conn.cursor()

#def getUserName():

def getName(email):
    sql = "select name from u_data where email=%s"
    mycursor.execute(sql, (email,))
    name = mycursor.fetchone()
    name = ''.join(name)

    return name


#def getPassword():



#def getAllData(Username, Password):

#def addProject():



#def removeProject():

def validateUser(email, password):
    sql = "select pass from u_data where email=%s"
    mycursor.execute(sql, (email,))
    c_pass = mycursor.fetchone()
    c_pass = ''.join(c_pass)

    if c_pass == password:
        return True
    else:
        return False

def create_user(username,name,email,password):
    sql = "INSERT INTO u_data (name, username, pass, email) VALUES (%s, %s, %s, %s)"
    val = (name,username,password, email)
    mycursor.execute(sql, val)
    conn.commit()

def create_database():
    mycursor.execute('CREATE DATABASE profydatabase;')
    conn.commit()
    mycursor.execute('USE profydatabase;')
    mycursor.execute('CREATE TABLE p_data (username TEXT,project TEXT);')
    conn.commit()
    mycursor.execute('CREATE TABLE u_data (name TEXT,username TEXT,pass TEXT,email TEXT);')
    conn.commit()

#Run This On First Run
#create_database()
#create_user("varunu311","Varun","varunu311@gmail.com","Upadhyay_12")