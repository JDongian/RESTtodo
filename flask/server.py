#!/srv/JDong.me/RESTtodo/venv/bin/python

import os
#TODO: remove the star eventually, when we figure out what we actually need.
from flask import *#Flask, jsonify
import flask_login
import dbtools

#Have the assets include properly for the HTML files by setting
#the static_folder for flask.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../flask/assets')
print ASSETS_DIR
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)

"""TODO: Set up login-manager for user sessions.
login_manager = LoginManager()
login_manager.init(app)

#Logins
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)
"""

###
#Helper functions
###
"""DEPRECATED
def valid_task(json):
    if 'value' in json.keys():
        return True
    return False
"""
def valid_schedule(json):
    #TODO: write a real validator
    if True:
        return True
    return False

###
#URL routing
###
@app.route('/', methods=['GET'])
def index():
    return open("assets/html/index.html", 'r').read()

@app.route('/schedule-planner', methods=['GET'])
def view_tasks():
    return open("assets/html/schedule_viewer.html", 'r').read()

###
#REST API endpoints (myEdu clone)
###
@app.route('/api/schedule', methods=['GET'])
def get_schedule():
#JUST A SAMPLE RESPONSE, THE DATABASE WILL BE HOOKED UP LATER.
    return {[
        {'title': "M325K"
        ,'description': "Discrete Mathematics"
        ,'days': "MWF"
        ,'timeslot': "1:00PM-2:00PM"},
        {'title': "M427K"
        ,'description': "Differential Equations"
        ,'days': "MWF"
        ,'timeslot': "2:00PM-3:00PM"},
        {'title': "M328K"
        ,'description': "Intro to Number Theory"
        ,'days': "MWF"
        ,'timeslot': "3:00PM-4:00PM"}
        ]}
    #return dbtools.get_schedule()

@app.route('/api/schedule', methods=['GET'])
def get_schedule():

#TODO: write all the other API endpoints.

"""DEPRECATED
#REST API (todo list)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    if id in tasks.keys():
        return jsonify({'task': tasks[id]})
    else:
        abort(404)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if valid_task(request.json):
        task = request.json.get('value', "")
        tasks[max(tasks.keys())+1] = task
        return jsonify({'new_task': task}, 201)
    else:
        abort(400)
"""

#Error handlers
@app.errorhandler(404)
def error404(error):
    return jsonify({'error': str(error)})

if __name__ == '__main__':
    #The server NEVER has debug on.
    app.run(debug=False, port=5000)
    #For debugging, the debug option is nice.
    #app.run(debug=True, port=5000)
