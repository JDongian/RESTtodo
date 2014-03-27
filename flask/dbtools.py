#!/srv/JDong.me/RESTtodo/venv/bin/python
"""Postgres database tools for REST API.

Usage:
    dbtools.py init [--users|--schedules]
    dbtools.py reset [--users|--schedules]
    dbtools.py delete [--users|--schedules]
    dbtools.py -h | --help
    dbtools.py --version

Options:
    -h --help       Show this screen.
    -v              Show version.
    --users         Only act on the users table.
    --schedules     Only act on the tasks table.
"""

from docopt import docopt
import os
import psycopg2

sqldir = "/srv/JDong.me/RESTtodo/sql/"

def get_cursor(level=0, db="restful", user=os.getlogin()):
    """Returns a cursor connected to the given database using given
    credentials. Default level 0 isolation level (autocommit on).
    """
    try:
        conn = psycopg2.connect("dbname={0} user={1}".format(db, user))
        #Execute all actions immediately
        #TODO: properly handle transacitons
        conn.set_isolation_level(level)
    except:
        print "Database connection failed."
    return conn.cursor()

def init_db(c, user=True, task=True):
    """Create user and todo tables.
    """
    if not user and not task:
        user, task = True, True
    if user:
        c.execute(open(sqldir+"user_schema.sql", 'r').read())
    if task:
        c.execute(open(sqldir+"schedule_schema.sql", 'r').read())

def delete_db(c, user=True, task=True):
    """Delete user and todo tables.
    """
    if not user and not task:
        user, task = True, True
    if user:
        c.execute(open(sqldir+"user_delete.sql", 'r').read())
    if task:
        c.execute(open(sqldir+"schedule_delete.sql", 'r').read())

def insert_user(c, email, fname, lname, pwdhash):
    c.execute(open("user_insert.sql", 'r').read(),
            {'email': email,
             'firstname': fname,
             'lastname': lname,
             'pwd': pwdhash})

"""
def insert_task(c, username, index, title, description, comments, state):
    c.execute(open("task_insert.sql", 'r').read(),
            {'username': username,
             'ord': index,
             'title': title,
             'description': description,
             'comments': comments,
             'state': state})
"""

def get_user():
    return False

def get_class():
    c.execute(open("schedule_select.sql", 'r').read(),)

if __name__ == '__main__':
    c = get_cursor()
    arguments = docopt(__doc__, version='REST edu 0.1')w
    if arguments['init']:
        init_db(c, arguments['--users'], arguments['--schedule'])
    elif arguments['reset']:
        delete_db(c, arguments['--users'], arguments['--schedule'])
        init_db(c, arguments['--users'], arguments['--schedule'])
    elif arguments['delete']:
        delete_db(c, arguments['--users'], arguments['--schedule'])
