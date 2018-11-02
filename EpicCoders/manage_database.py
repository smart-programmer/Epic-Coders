from EpicCoders import app, db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# https://flask-migrate.readthedocs.io/en/latest/

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
