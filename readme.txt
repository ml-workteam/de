1. Django Webapp
2. Kafka
3. ClickHouse
4. Запуск демонстрации
5. Анализ активности согласно ТЗ


1. Django Webapp
----------------


1.1. Склонировать код из репозитория https://github.com/ml-workteam/de.git
1.2. cd в папку с репозиторием
1.3. python -m venv env
1.4. source env/bin/activate
1.5. pip install -r requirements.txt

1.6. cd webapp
1.7. python manage.py runserver



2. Kafka
--------

2.1. Скачать дистрибутив с kafka.apache.org версия 2.4.1 (scala 2.11)
https://archive.apache.org/dist/kafka/2.4.1/kafka_2.11-2.4.1.tgz

2.2. разархивировать в kafka
tar -xzf kafka_2.11-2.4.1.tgz
cd kafka_2.11-2.4.1

2.3. В отдельном окне терминала запустить ZooKeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

2.4. В отдельном окне терминала запустить Kafka
bin/kafka-server-start.sh config/server.properties

2.5. Создать в Kafka топик events
bin/kafka-topics.sh --create --topic events --bootstrap-server localhost:9092

2.6. В отдлеьном окне терминала запустить консольного потребителя кафки
bin/kafka-console-consumer.sh --topic events --bootstrap-server localhost:9092

2.7. В отдельном окне терминала запустить Producer (RDBMS -> Kafka)
cd kafka-producer
python producer.py



3. ClickHouse
-------------

3.1. Установить ClickHouse
3.1.  Выполнить DDL скрипты из clickhouse/ddl.sql



4. Запуск пайплайна
------------------- 

4.1. cd simulations

4.2. Сгенерировать пользователей
python generate_users.py

4.3. Сгенерировать задачи
python generate_tasks.py

4.4. Генератор событий
python simulator.py


5. Отчет
--------

5.1. Запрос из clickhouse/report.sql
5.2. Доступ в админку Django workteam/123456



Демонстрация запуска и защита задания в видео на youtube:

1. Запуск: https://youtu.be/0FseHZWM08o
2. Проблемы на Кафке: https://youtu.be/6EIN5_A1oCo
3. Проблемы на продюсере и на кликхаусе: https://youtu.be/4kQU2hbHPaY
4. Убеждаемся, что все данные на месте: https://youtu.be/qm34mOUu1_M

