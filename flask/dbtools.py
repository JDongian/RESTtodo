#!/srv/JDong.me/RESTtodo/venv/bin/python
"""Postgres database tools for REST API.

Usage:
    dbtools.py init [--users|--tasks]
    dbtools.py reset [--users|--tasks]
    dbtools.py delete [--users|--tasks]
    dbtools.py -h | --help
    dbtools.py --version

Options:
    -h --help       Show this screen.
    -v              Show version.
    --users         Only act on the users table.
    --tasks         Only act on the tasks table.
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
        c.execute(open(sqldir+"task_schema.sql", 'r').read())

def delete_db(c, user=True, task=True):
    """Delete user and todo tables.
    """
    if not user and not task:
        user, task = True, True
    if user:
        c.execute(open(sqldir+"user_delete.sql", 'r').read())
    if task:
        c.execute(open(sqldir+"task_delete.sql", 'r').read())

if __name__ == '__main__':
    c = get_cursor()
    arguments = docopt(__doc__, version='REST todo 0.1')
    if arguments['init']:
        init_db(c, arguments['--users'], arguments['--tasks'])
    elif arguments['reset']:
        delete_db(c, arguments['--users'], arguments['--tasks'])
        init_db(c, arguments['--users'], arguments['--tasks'])
    elif arguments['delete']:
        delete_db(c, arguments['--users'], arguments['--tasks'])
