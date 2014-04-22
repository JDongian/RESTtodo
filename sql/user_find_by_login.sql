SELECT email FROM users WHERE
    email=%(email)s
AND pwd=%(hash)s
AND status=0;
