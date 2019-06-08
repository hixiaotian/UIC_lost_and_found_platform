from flask import Flask, render_template
from app.config import config
from app.extensions import config_extensions
from app.views import config_blueprint





# Encapsulate the action of creating an app as a function
def create_app(config_name):
    # Create the app instance object
    app = Flask(__name__)
    # Load Configuration
    app.config.from_object(config.get(config_name) or 'default')
    # Perform additional initialization
    config.get(config_name).init_app(app)


    #set debug=True,let toolbar take effect
    # app.debug=True

    # Extension Loader
    config_extensions(app)

    # Configure a blueprint
    config_blueprint(app)

    # return app Instance Objects
    return app