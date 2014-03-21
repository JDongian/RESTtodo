INSERT INTO schedule (
 username
,title
,description
,days
,timeslot
) VALUES (
 %(username)s
,%(title)s
,%(description)s
,%(days)s
,%(timeslot)s
);
