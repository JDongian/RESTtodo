DELETE FROM schedules
WHERE username=%(email)s
AND title=%(title)s
AND description=%(descr)s;
