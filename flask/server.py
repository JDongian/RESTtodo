#!/srv/JDong.me/RESTtodo/venv/bin/python

import os
from flask import *#Flask, jsonify

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../flask/assets')
print ASSETS_DIR
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)

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

@app.route('/view', methods=['GET'])
def view_tasks():
    return open("assets/html/view_all.html", 'r').read()

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

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if valid_task(request.json):
        task = request.json.get('value', "")
        tasks[max(tasks.keys())+1] = task
        return jsonify({'new_task': task}, 201)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
