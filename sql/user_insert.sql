INSERT INTO users (
 email
,firstname
,lastname
,pwd
) VALUES (
 %(email)s
,%(firstname)s
,%(lastname)s
,%(pwd)s
);
