SELECT title, description, days, timeslot
FROM schedules
WHERE username=%(email)s;
