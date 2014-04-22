SELECT pwd FROM users WHERE
    email=%(email)s
AND firstname=%(fname)s
AND lastname=%(lname)s;
