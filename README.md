# FlaskRabbit
Python 3.6.5, Postgresql 10

Simple CRUD app based on flask and rabbitmq.
At the moment works syncroniously.

0)
cd ~/FlaskRabbit
pip install -r requirements.txt

1) Add your database (e.g postgresql):

Consumer_service/settings.py

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
                                                                    

2) Choose server and port

Consumer_service/settings.py
API_service/settings.py

e.g:

FLASK_SERVER_NAME = 'your_host:your_port'

3) python run_api_service.py
4) python run_consumer_service.py
5) open your host/api/
