INSERT INTO tasks (
 username
,ord
,title
,description
,comments
,state
) VALUES (
 %(username)s
,%(ord)s
,%(title)s
,%(description)s
,%(comments)s
,%(state)s
);
