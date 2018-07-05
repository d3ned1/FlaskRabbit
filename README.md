# FlaskRabbit
Python 3.6.5, PostgreSQL 10

Simple CRUD app based on Flask and RabbitMQ.

0) "cd ~/FlaskRabbit", create virtual environment, "pip install -r requirements.txt"

1.1) Add your database (e.g postgresql):

Consumer_service/consumer_settings.py

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'mydb'
USER = 'postgres'
PASSWORD = 'password'

SQLALCHEMY_DATABASE_URI = "postgresql://{0}:{1}@{2}:{3}/{4}".format(USER,
                                                                    PASSWORD,
                                                                    DB_HOST,
                                                                    DB_PORT,
                                                                    DB_NAME)

1.2) Add Redis settings:

REDIS_HOST = 'localhost',
REDIS_DB = 15,
REDIS_PORT = 6379                                                                    

2.1) Choose server and port

Consumer_service/settings.py
API_service/settings.py

e.g:

FLASK_SERVER_NAME = 'your_host:your_port'

2.2) Migrate to database:
python migrate.py db init;
python migrate.py db migrate;
python migrate db upgrade

3) Run apps:
3.1) python run_api_service.py
3.2) python run_consumer_service.py

4.1) Open your host/api/movies to make a request. As a response you will get the UUID.
4.2) Open your host/api/get_result/<UUID> to get the actual data you requested.
