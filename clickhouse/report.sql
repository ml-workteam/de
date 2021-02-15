select day, groupArray(tuple(action_id, unique_users))
from (
    select toYYYYMMDD(time) as day, action_id, count(distinct user_id) as unique_users
    from events
    group by toYYYYMMDD(time), action_id) tbl
group by day
order by day;

