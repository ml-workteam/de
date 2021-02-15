conf = {
    'db_path': '../webapp/db.sqlite3',
    'bootstrap_servers' : ['localhost:9092'],
    'query': """
        select
            e.id event_id,
            e.time,
            e.user_id,
            u.join_date,
            u.registration_date,
            u.name,
            u.email,
            u.is_guest,
            e.target_id step_id,
            e.action_id
        from edu_event e
            inner join edu_user u on e.user_id = u.id
        where e.id > {0}    
        order by e.id
        """,
    'get_last_query' : """
        select max_id from edu_producerlog order by max_id desc limit 1
    """ ,
    'insert_producerlog_query' : """
        insert into edu_producerlog (min_id, max_id, producer_id, ts, status, has_errors) values (:min_id, :max_id, :producer_id, :ts, :status, :has_errors)
    """
}