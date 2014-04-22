#!/srv/JDong.me/RESTtodo/venv/bin/python
"""Postgres database tools for REST API.

Usage:
    dbtools.py init [--users|--schedules]
    dbtools.py reset [--users|--schedules]
    dbtools.py delete [--users|--schedules]
    dbtools.py sampleadd [--users][--schedules]
    dbtools.py -h | --help
    dbtools.py --version

Options:
    -h --help       Show this screen.
    -v              Show version.
    --users         Only act on the users table.
    --schedules     Only act on the tasks table.
"""

import random
from faker import Faker
from docopt import docopt
import os
import psycopg2

sqldir = "/srv/JDong.me/RESTtodo/sql/"
sqldir = "../sql/"

def hash_pass(p):
    return hash(p)

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
    data = {'email': email,
            'fname': fname,
            'lname': lname,
            'pwd': pwdhash}
    return c.execute(open(sqldir+"user_insert.sql", 'r').read(), data)

def insert_schedule(c, username, title, description, days, timeslot):
    c.execute(open(sqldir+"schedule_insert.sql", 'r').read(),
            {'username': username,
             'title': title,
             'description': description,
             'days': days,
             'timeslot': timeslot})

def fetch_user_all(c):
    c.execute(open(sqldir+"user_selectall.sql", 'r').read())
    return c.fetchall()

def search_user_by_match(c, email, fname, lname):
    c.execute(open(sqldir+"user_find_by_match.sql", 'r').read(),
              {'email': email,
               'fname': fname,
               'lname': lname})
    return c.fetchall()

def user_valid_login(c, email, hash):
    c.execute(open(sqldir+"user_find_by_login.sql", 'r').read(),
              {'email': email,
               'hash': hash})
    status = len(c.fetchall())
    if status > 1:
        print "ERROR?"
    return status == 1

def search_user_by_email(c, email):
    c.execute(open(sqldir+"user_find_by_email.sql", 'r').read(), email)
    return c.fetchall()

def fetch_user(c):
    return False

def fetch_classes(c, user):
    c.execute(open(sqldir+"schedule_select.sql", 'r').read(), user)

def set_user_fresh(c, email):
    c.execute(open(sqldir+"user_set_fresh.sql", 'r').read(),
              {'email': email})

if __name__ == '__main__':
    f = Faker()
    c = get_cursor()
    arguments = docopt(__doc__, version='REST edu 0.1')
    if arguments['init']:
        init_db(c, arguments['--users'], arguments['--schedules'])
    elif arguments['reset']:
        delete_db(c, arguments['--users'], arguments['--schedules'])
        init_db(c, arguments['--users'], arguments['--schedules'])
    elif arguments['delete']:
        delete_db(c, arguments['--users'], arguments['--schedules'])
    elif arguments['sampleadd']:
        if(arguments['--users']):
            for i in xrange(8):
                insert_user(c,
                        f.email(),
                        f.name().split()[0],
                        f.name().split()[1],
                        hash_pass(f.zip_code()))
        if(arguments['--schedules']):
            for i in xrange(8):
                insert_schedule(c,
                        random.choice([r[0] for r in fetch_user_all(c)]),
                        random.choice(['M', 'CS'])+str(random.randint(100,900)),
                        "Some herpy example class",
                        random.choice(["MWF", "TuTh"]),
                        "8:00-9:00")
