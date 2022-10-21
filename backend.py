import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Your Password Goes Here ",
    database = "profydatabase"
)

mycursor = mydb.cursor()

#def getUserName():

#def getPassword():

#def getAllData(Username, Password):

def validateUser(email, password):
    sql = "select pass from u_data where email=%s"
    mycursor.execute(sql, (email,))
    c_pass = mycursor.fetchone()
    c_pass = ''.join(c_pass)

    if c_pass == password:
        return True
    else:
        return False

def create_user(email, password):
    sql = "INSERT INTO u_data (email, pass) VALUES (%s, %s)"
    val = (email, password)
    mycursor.execute(sql, val)
    mydb.commit()