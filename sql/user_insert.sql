INSERT INTO users (
 email
,firstname
,lastname
,pwd
,status
) VALUES (
 %(email)s
,%(fname)s
,%(lname)s
,%(pwd)s
,1
);
