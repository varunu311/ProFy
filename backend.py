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
    mc.execute(sql, email)
    data = mc.fetchall()
    data = data.replace(",","").replace("(","").replace(")","")
    print(data)
    return data

def getAllProjects(username):
    sql = "select DISTINCT project from p_data where username=%s"
    mc.execute(sql, (username,))
    projects = mc.fetchall()
    projects = [pro for x in projects for pro in x]
    print(projects)
    return projects

def getAllTasks(username, project):
    sql = "select task from p_data where username=%s AND project=%s"
    mc.execute(sql, (username,project))
    tasks = mc.fetchall()
    tasks = [pro for x in tasks for pro in x]
    
    while "none" in tasks:
        tasks.remove("none")

    print(tasks)
    return tasks

def addProject(username, project):
    print(project)
    sql = "INSERT INTO p_data (username, project, task) VALUES (%s, %s, %s);"
    val = (username,project,"none")
    mc.execute(sql,val)
    conn.commit
    print("Done")

def addTask(username, project, task):
    sql = "select username from u_data"
    mc.execute(sql, (username,))
    u = mc.fetchall()
    u = [pro for x in u for pro in x]

    sql = "select task from p_data where username=%s AND project=%s"
    mc.execute(sql, (username,project, ))
    t = mc.fetchall()
    #t = ''.join(t)
    t= [pro for x in t for pro in x]

    if username in u: 
        
        if task not in t:
            sql = "INSERT INTO p_data (username, project, task) VALUES (%s, %s, %s);"
            val = (username,project,task)
            mc.execute(sql,val)
            conn.commit
            print(task, "Successfully Added To", project)
        else:
            print("This Task Already Exists In the Project")
    else:
        print("This User Does Not Exist")


def removeProject(username,project):
    sql = "DELETE FROM p_data WHERE username=%s AND project=%s"
    val = (username,project)
    mc.execute(sql,val)
    conn.commit
    print("Done")

def removeTask(username,project, task):
    sql = "DELETE FROM p_data WHERE username=%s AND project=%s AND task =%s"
    val = (username,project,task)
    mc.execute(sql,val)
    conn.commit
    print("Done")

def editTask(username, project, old_task, new_task):
    sql = "UPDATE p_data SET task=%s WHERE username=%s AND project=%s AND task=%s;"
    val = (new_task,username, project, old_task)
    mc.execute(sql,val)
    conn.commit
    print("Done")

def editProject(username,old_project,new_project):
    sql = "UPDATE p_data SET project=%s WHERE username=%s AND project=%s;"
    val = (new_project,username, old_project)
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
    
    sql = "select email from u_data where email=%s"
    mc.execute(sql, (email,))
    e_mail = mc.fetchone()

    if c_pass is None:
        return False
    else: 
        c_pass = ''.join(c_pass)
        if c_pass == password:
            return True
        else:
            return False

def create_user(username,name,email,password):
    sql = "select username from u_data where username=%s"
    mc.execute(sql, (username,))
    u_name = mc.fetchone()
    
    sql = "select email from u_data where email=%s"
    mc.execute(sql, (email,))
    e_mail = mc.fetchone()
    
    if u_name is None and e_mail is None:
        sql = "INSERT INTO u_data (name, username, pass, email) VALUES (%s, %s, %s, %s)"
        val = (name,username,password, email)
        mc.execute(sql, val)
        conn.commit()
        print("Account Created Successfully")
        return True
    else:
        print("Account Already Exists")
        return False

def get_task_datetime(email, project, task): 
    sql = "SELECT datetime FROM p_data where email=%s and project=%s and task=%s" 
    val = (email,project, task)
    mc.execute(sql, val)
    mc.fetchone()
    return datetime
def create_database():
    mc.execute('CREATE DATABASE profydatabase;')
    conn.commit()
    mc.execute('USE profydatabase;')
    mc.execute('CREATE TABLE p_data (username TEXT,project TEXT, task TEXT);')
    conn.commit()
    mc.execute('CREATE TABLE u_data (name TEXT,username TEXT,pass TEXT,email TEXT);')
    conn.commit()
    print("Done")

#Run This On First Run
#create_database()
#create_user("Diya123","Diya Patel", "diya@gmail.com", "app123")
#create_user("Varunu311","Varun Upadhyay","varunu311@gmail.com","Upadhyay_12")
#create_user("Varunu211","vu","varunu211@gmail.com","Upadhyay_12")
#addProject("varunu311","Software Development")
#addProject("varunu311","Web Development")
#getAllProjects("varunu311")
#addProject("varunu311", "ProFy")
#getAllProjects("varunu311")
#addTask("varunu311", "ProFy", "Frontend")
#addTask("Varunu211", "ProFy", "Frontend")
#getAllTasks("varunu311", "ProFy")