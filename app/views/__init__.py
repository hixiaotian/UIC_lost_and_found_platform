from .main import main
from .user import user
from .item import item

DEFAULT_BLUEPRINT = (
    (main, ''),
    (user, '/user'),
    (item, '/item')
)

# Functions that encapsulate the configuration blueprint
def config_blueprint(app):
    # The loop reads the blueprint in the tuple
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)
