from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.movie import db
from run_consumer_service import initialize_app, app

app = initialize_app(app, migrate=True)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
