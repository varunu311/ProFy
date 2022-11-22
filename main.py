import os                 
import backend
from flask import session
from flask import Flask  
from flask import render_template, redirect, url_for, request


app = Flask(__name__)     # create an app
app.secret_key = "XWK09182TYPK01W"


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page

########################################################## HOME PAGE #########################################################
@app.route('/')
def main():
    return render_template('home.html')

@app.route('/home')
def home():
    if "email" in session:
        return redirect(url_for("view"))
    else: 
        return render_template('home.html')

########################################################## SIGN_IN PAGE #########################################################
@app.route('/Sign_In', methods=["POST","GET"])
def Sign_In():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["pass"]
        if backend.validateUser(email, password) == True:
            session["email"] = email
            return redirect(url_for("view"))
        else:
            print("Login Failed: Password and Email do not match/Exist")
            return render_template('Sign_in.html')
    else:
        return render_template('Sign_in.html')


@app.route('/signout')
@app.route('/logout')
def signout():
    session.pop('email')
    return redirect(url_for("Sign_In"))
    
########################################################## USER PAGE #########################################################
@app.route("/view", methods=["POST","GET"])
def view():
    if "email" in session:
        email = session["email"]
        u_name = backend.getUsername(email)
        name = backend.getName(email)

        if request.method == "POST":
            return render_template('view.html',name = backend.getName(email), username = u_name, projects = backend.getAllProjects(u_name))
        
        else:
            return render_template('view.html', name = backend.getName(email),username = u_name, projects = backend.getAllProjects(u_name))
    else:
        return redirect(url_for("Sign_In"))

@app.route("/viewsorted", methods=["POST", "GET"])
def viewsorted():
    if "email" in session:
        email = session["email"]
        u_name = backend.getUsername(email)
        name = backend.getName(email)
        projects = backend.getAllProjects(u_name)
        sortedproject = projects.sort()
        print(sortedproject)

        if request.method == "POST":
            return render_template('view.html',name = backend.getName(email), username = u_name, projects = projects)
        
        else:
            return render_template('view.html', name = backend.getName(email),username = u_name, projects = projects)
    else:
        return redirect(url_for("Sign_In"))


@app.route("/view/<project>", methods=["POST","GET"])
def viewproject(project):
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        return render_template('viewproject.html', tasks = backend.getAllTasks(username, project))
    else:
        return redirect(url_for("Sign_In"))
    
########################################################## SIGN_UP PAGE #########################################################
@app.route('/Sign_Up', methods=["POST","GET"])
@app.route('/Register', methods=["POST","GET"])
def Sign_Up():
    if request.method == "POST":
        name = request.form["name"]
        username = (request.form["username"]).lower()
        email = (request.form["email"]).lower()
        password = request.form["pass"]
        c_password = request.form["c_pass"]

        if c_password == password:
            if backend.create_user(username, name, email, password) == True:
                return redirect(url_for("Sign_In"))
            else:
                return render_template('Sign_up.html')
        else: 
            print("Passwords Did Not Match")
            return render_template('Sign_up.html')
    else:
        return render_template('Sign_up.html')

@app.route('/ap', methods=["POST","GET"])
def ap():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        
        if request.method == "POST":
            project = request.form["project"]
            backend.addProject(username, project)
            print("Project Created")
            backend.getAllProjects(username)
            return render_template('ap.html')
        
        else:
            return render_template('ap.html')

    return redirect(url_for("view"))

@app.route('/rp', methods=["POST","GET"])
def rp():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        
        if request.method == "POST":
            project = request.form["project"]
            backend.removeProject(username, project)
            print("Project Removed")
            backend.getAllProjects(username)
            return render_template('rp.html')
        
        else:
            return render_template('rp.html')
            
    return redirect(url_for("view"))

@app.route('/at', methods=["POST","GET"])
def at():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        
        if request.method == "POST":
            project = request.form["project"]
            task = request.form["task"]
            backend.addTask(username, project, task)
            print("Task Added")
            backend.getAllTasks(username, project)
            return render_template('at.html')
        
        else:
            return render_template('at.html')
            
    return redirect(url_for("view"))

@app.route('/rt', methods=["POST","GET"])
def rt():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        
        if request.method == "POST":
            project = request.form["project"]
            task = request.form["task"]
            backend.removeTask(username, project, task)
            print("Task Removed")
            backend.getAllTasks(username, project)
            return render_template('rt.html')
        
        else:
            return render_template('rt.html')
            
    return redirect(url_for("view"))

@app.route('/ep', methods=["POST","GET"])
def ep():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        name = backend.getName(email)
        
        if request.method == "POST":
            old_project = request.form["old_project"]
            new_project = request.form["new_project"]
            backend.editProject(username, old_project, new_project)
            print("Project Edited")
            backend.getAllProjects(username)
            return render_template('ep.html')
        
        else:
            return render_template('ep.html')
            
    return redirect(url_for("view"))

@app.route('/et', methods=["POST","GET"])
def et():
    if "email" in session:
        email = session["email"]
        username = backend.getUsername(email)
        
        if request.method == "POST":
            project = request.form["project"]
            old_task = request.form["old_task"]
            new_task = request.form["new_task"]
            backend.editTask(username, project, old_task, new_task)
            print("Task Edited")
            backend.getAllTasks(username, project)
            return render_template('et.html')
        
        else:
            return render_template('et.html')
            
    return redirect(url_for("view"))

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5001)),debug=True)