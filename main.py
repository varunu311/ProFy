import os                 # os is used to get environment variables IP & PORT
import backend
import secrets
from flask import session
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template, redirect, url_for, request


app = Flask(__name__)     # create an app
app.secret_key = "XWK09182TYPK01W"

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/Sign_In', methods=["POST","GET"])
def Sign_In():
    if request.method == "POST":
        email = (request.form["email"]).lower()
        password = request.form["pass"]
        if backend.validateUser(email, password) == True:
            session["email"] = email
            return redirect(url_for("user"))
        else:
            print("Login Failed: Password and Email do not match/Exist")
            return render_template('Sign_in.html')
    else:
        return render_template('Sign_in.html')

@app.route("/Logged_In", methods=["POST","GET"])
def user():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        print(username)
        if request.method == "POST":
            if request.method['field'] == "addProject":
                project = request.form["project"]
                print(project)
                backend.addProject(username, project)
                print("Project successfully Added!!!")
                return render_template('User.html')
            else: 
                print("hey")
                return render_template('User.html')
        else:
            return render_template('User.html')

    else:
        return redirect(url_for("Sign_In"))


@app.route('/Sign_Up', methods=["POST","GET"])
@app.route('/Register', methods=["POST","GET"])
def Sign_Up():
    if request.method == "POST":
        name = request.form["name"]
        username = (request.form["username"]).lower()
        email = (request.form["email"]).lower()
        password = request.form["pass"]
        if backend.create_user(username, name, email, password) == True:
            print("Successfully created")
            return redirect(url_for("Sign_In"))
        else:
            return render_template('Sign_up.html')
    else:
        return render_template('Sign_up.html')

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)