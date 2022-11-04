import psycopg2
import os

conn = psycopg2.connect('postgresql://profy:TRscICM9vdVHM9D-U9M1xw@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/profydatabase?sslmode=verify-full&options=--cluster%3Dbeige-cuscus-6334')
mc = conn.cursor()

#def getUserName():

def getName(email):
    sql = "select name from u_data where email=%s"
    mc.execute(sql, (email,))
    name = mc.fetchone()
    name = ''.join(name)
    print(name)
    return name


def getPassword(email):
    sql = "select password from u_data where email=%s"
    mc.execute(sql, (email,))
    password = mc.fetchone()
    password = ''.join(password)
    return password

def getAllData(email):
    sql = "select * from u_data where email=%s"
    mc.execute(sql, (email,))
    data = mc.fetchall()
    print(data)
    return data

def getAllProjects(username):
    sql = "select project from p_data where username=%s"
    mc.execute(sql, (username,))
    projects = mc.fetchall()
    print(projects)
    return projects

def addProject(username, project):
    sql = "INSERT INTO p_data (username, project) VALUES (%s, %s)"
    val = (username,project)
    mc.execute(sql,val)
    conn.commit
    print("Done")

#def removeProject():
def removeProject(username,project):
    sql = "DELETE FROM p_data WHERE username=%s AND project=%s"
    val = (username,project)
    mc.execute(sql,val)
    conn.commit
    print("Done")

def getUsername(email):
    sql = "select username from u_data where email=%s"
    mc.execute(sql, (email,))
    username = mc.fetchone()
    username = ''.join(username)
    return username


def validateUser(email, password):
    sql = "select pass from u_data where email=%s"
    mc.execute(sql, (email,))
    c_pass = mc.fetchone()
    c_pass = ''.join(c_pass)

    if c_pass == password:
        return True
    else:
        return False

def create_user(username,name,email,password):
    sql = "INSERT INTO u_data (name, username, pass, email) VALUES (%s, %s, %s, %s)"
    val = (name,username,password, email)
    mc.execute(sql, val)
    conn.commit()
    print("Done")

def create_database():
    mc.execute('CREATE DATABASE profydatabase;')
    conn.commit()
    mc.execute('USE profydatabase;')
    mc.execute('CREATE TABLE p_data (username TEXT,project TEXT);')
    conn.commit()
    mc.execute('CREATE TABLE u_data (name TEXT,username TEXT,pass TEXT,email TEXT);')
    conn.commit()
    print("Done")

#Run This On First Run
#create_database()
#create_user("varunu311","Varun","varunu311@gmail.com","Upadhyay_12")