#!/srv/JDong.me/RESTtodo/venv/bin/python

import os
from flask import *#Flask, jsonify
import flask_login

#Have the assets include properly for the HTML files by setting
#the static_folder for flask.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../flask/assets')
print ASSETS_DIR
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)

"""
#Set up login-manager for user sessions.
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

#REST API

#ordered list of tasks, to be replaced with database.
tasks = {
        1: 'buy things',
        2: 'sell things'
}

def valid_task(json):
    if 'value' in json.keys():
        return True
    return False

@app.route('/', methods=['GET'])
def index():
    return open("assets/html/index.html", 'r').read()

@app.route('/viewall', methods=['GET'])
def view_tasks():
    return open("assets/html/viewall.html", 'r').read()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    if id in tasks.keys():
        return jsonify({'task': tasks[id]})
    else:
        abort(404)

@app.errorhandler(404)
def error404(error):
    return jsonify({'error': str(error)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if valid_task(request.json):
        task = request.json.get('value', "")
        tasks[max(tasks.keys())+1] = task
        return jsonify({'new_task': task}, 201)
    else:
        abort(400)

@app.route('/api/tasks/swap/', methods=['POST'])
def swap_tasks():
    if valid_task(request.json):
        task = request.json.get('value', "")
        tasks[max(tasks.keys())+1] = task
        return jsonify({'new_task': task}, 201)
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
