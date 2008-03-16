#!/srv/JDong.me/RESTtodo/venv/bin/python

import os
#TODO: remove the star eventually, when we figure out what we actually need.
from flask import *#Flask, jsonify
import flask_login
from getpass import getpass
import smtplib
import dbtools

#Have the assets include properly for the HTML files by setting
#the static_folder for flask.
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '../flask/assets')
print ASSETS_DIR
app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
sender = 'jdong42@gmail.com'
js_maxval = 9007199254740991

c = dbtools.get_cursor()

###
#Helper functions
###
def valid_schedule(json):
    #TODO: write a real validator
    if True:
        return True
    return False

def secure_hash(d):
    #herp...
    return hash(d)

def valid_signup(args):
    if args['k'] == 'key':
        h = dbtools.search_user_by_match(c,
                args['email'], args['fname'], args['lname'])
        if len(h) != 0:
            state = (h[0][0] == long(args['h']))
            return state
    return False

def send_acc_create(recipient, name, pwd_hash):
    subject = 'Welcome to your new Classeract account!'
    body = """Hi %s,<br>
You've created a new account on Classeract! To confirm your account, please follow the URL below:<br>
<a href='http://flask.jdong.me/api/confirm/?k=%s&email=%s&h=%s&fname=%s&lname=%s'>confirm account</a><br>
<br>
Cheers,<br>
The Classeract Team
""" % (name, 'key', recipient, pwd_hash, name.split()[0], name.split()[1])
    headers = ["From: classeract@flask.jdong.me",
            "Subject: " + subject,
            "To: " + recipient,
            "MIME-Version: 1.0",
            "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, pwd)
    try:
        session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    except:
        session.quit()
        return 1
    session.quit()
    return 0

###
#URL routing
###
@app.route('/', methods=['GET'])
def page_index():
    return open("assets/html/index.html", 'r').read()

@app.route('/signup', methods=['GET'])
def page_signup():
    return open("assets/html/newuser.html", 'r').read()

#The demo page for the first showing
@app.route('/cs326e', methods=['GET'])
def page_cs3263():
    return open("assets/html/cs326e.html", 'r').read()

#View all classes
@app.route('/schedule-planner', methods=['GET'])
def page_viewer():
    return open("assets/html/schedule_viewer.html", 'r').read()

###
#REST API endpoints (myEdu clone)
###

#SCHEDULE ENDPOINTS

@app.route('/api/schedule/full', methods=['POST'])
def get_schedule():
    if check_login(request.form) == 0:
        d = dbtools.fetch_schedule_by_email(c, request.form['email'])
        d = {'schedule':
         [{'title': row[0]
          ,'description': row[1]
          ,'days': row[2]
          ,'timeslot': row[3]} for row in d], 
         'status': 0}
        return jsonify(d)
    else:
        #bad login
        return jsonify({'status': -1, 'schedule': []})

@app.route('/api/schedule/single', methods=['GET'])
def get_schedule_item():
#JUST A SAMPLE RESPONSE, THE DATABASE WILL BE HOOKED UP LATER.
    return jsonify({'item':
        {'title': "M325K"
        ,'description': "Discrete Mathematics"
        ,'days': "MWF"
        ,'timeslot': "1:00PM-2:00PM"}})

@app.route('/api/schedule/addclass', methods=['POST'])
def add_class():
    if check_login(request.form) == 0:
        dbtools.insert_schedule(c,
                request.form['email'],
                request.form['title'],
                request.form['descr'],
                request.form['days'],
                request.form['time'])
        return jsonify({'status': 0})
    else:
        #bad login
        return jsonify({'status': -1})

@app.route('/api/schedule/delete', methods=['POST'])
def delete_class():
    if check_login(request.form) == 0:
        print c, request.form
        dbtools.delete_schedule(c,
                request.form['email'],
                request.form['title'],
                request.form['descr'])
        print c, request.form
        return jsonify({'status': 0})
    else:
        #bad login
        return jsonify({'status': -1})

#USER ENDPOINTS

@app.route('/api/login', methods=['POST'])
def validate_login():
    """Takes in a pwd and email arg in the POST form and returns a JSON with
    the key 'status' holding the result of the login.
    """
    h = secure_hash(request.form['pwd'])
    if dbtools.user_valid_login(c, request.form['email'], h):
        return jsonify({'status': h%js_maxval})
    return jsonify({'status': -1})

@app.route('/api/validate', methods=['POST'])
def check_login(f=None):
    if f:
        e = f['email']
        p = f['pwd']
    else:
        e = request.form['email']
        p = request.form['pwd']
    h = dbtools.search_user_by_email(c,
            {'email': e})[0][3]
    if h%js_maxval == long(p):
        if f:
            return 0
        else:
            return jsonify({'status': 0})
    if f:
        return -1
    else:
        return jsonify({'status': -1})

@app.route('/api/adduser', methods=['POST'])
def email_confirm():
    h = secure_hash(request.form['pwd'])
    #Send an Email to the user to confirm account.
    status = send_acc_create(request.form['email'],
                             request.form['fname']+' '+request.form['lname'],
                             h)
    #Add a database entry for server confirmation.
    try:
        dbtools.insert_user(c,
                            request.form['email'],
                            request.form['fname'],
                            request.form['lname'],
                            h)
    except:
        return jsonify({'status': 2})
    return jsonify({'status': status})

@app.route('/api/confirm/', methods=['GET'])
def try_net_acc():
    if valid_signup(request.args):
        #Validate account state from 1 to 0.
        dbtools.set_user_fresh(c, request.args['email'])
        return open("assets/html/new_acc_success.html", 'r').read()
    return 'Account creation failed. If you think this was an error,\
please email the  administrator.'

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

pwd = getpass("password: ")
if __name__ == '__main__':
    #The server NEVER has debug on.
    #app.run(debug=False, port=5000)
    #For debugging, the debug option is nice.
    app.run(debug=True, port=5001)
