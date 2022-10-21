import os                 # os is used to get environment variables IP & PORT
import backend
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template, redirect, url_for, request


app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/signin', methods=["POST","GET"])
def Sign_In():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        if backend.validateUser(email, password) == True:
            return redirect(url_for("user",usr=email))
        else:
            print("Login Failed: Password and Email do not match")
            return render_template('Sign_in.html')
    else:
        return render_template('Sign_in.html')

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route('/signup')
@app.route('/register')
def Sign_Up():
    return render_template('register.html')

@app.route('/logged_in')
def landing_page():
    return f"<h1>Log In Successful<h1/>"

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)