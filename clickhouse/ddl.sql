-- таблица - consumer
create table events_queue (
    `event_id` UInt64,
    `time` DateTime64,
    `user_id` UInt64,
    `join_date` DateTime64,
    `registration_date` DateTime64,
    `name` String,
    `email` String,
    `is_guest` Int8,
    `step_id` UInt64,
    `action_id` Int8
  ) engine = Kafka settings kafka_broker_list = 'localhost:9092',
                            kafka_topic_list = 'events',
                            kafka_group_name = 'clickhouse2',
                            kafka_format = 'JSONEachRow',
                            kafka_num_consumers = 1;

-- 
-- аналитическая таблица (материализованне представление)
-- (убираем event_id, уникализируем строки - на случай дублирования при сбоях очереди)
create table events (
    `time` DateTime64,
    `user_id` UInt64,
    `join_date` DateTime64,
    `registration_date` DateTime64,
    `name` String,
    `email` String,
    `is_guest` Int8,
    `step_id` UInt64,
    `action_id` Int8
) engine = MergeTree()
partition by toYYYYMM(time)
order by (toYYYYMM(time));

create materialized view events_view to events
    as select `time`, `user_id`, `join_date`, `registration_date`, `name`, `email`, `is_guest`, `step_id`, `action_id`
    from (select distinct * from events_queue) as tbl;


