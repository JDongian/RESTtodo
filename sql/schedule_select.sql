SELECT schedules.title, schedules.description

 username       text
,title          text
,description    text
,days           text
,timeslot       time
)


FROM schedules
JOIN schedules
ON hint_hash.hash_id = %(hash_id)s
AND hint_hash.hint_id = hint_data.hint_id
AND hint_data.hint IS NOT NULL;
