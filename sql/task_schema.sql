CREATE TABLE IF NOT EXISTS tasks(
 hint_id        serial PRIMARY KEY
,username       text
,ord            int
,title          text
,description    text
,comments       text
,state          bool
);
