from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from change_demo import app
from exts import db
from models import impact_list

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == 'main':
    manager.run()