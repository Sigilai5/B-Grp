from app import app
from flask_script import Migrate, MigrateCommand
from flask_script import manager

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
