from jinja2 import Environment

from app import create_app
from flask_script import Manager, Server
import os
from flask_migrate import MigrateCommand
# Get from the environment variable config_name
config_name = os.environ.get('FLASK_CONFIG') or 'default'

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
# generate app
app = create_app(config_name)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
manager = Manager(app)

manager.add_command('db',MigrateCommand)
manager.add_command('runserver', Server(use_debugger=True))

if __name__ == '__main__':
    manager.run()
