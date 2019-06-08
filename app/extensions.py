from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
# create object

db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)
# initialize
def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    # Some picture upload configuration
    configure_uploads(app, photos)
    # Set the upload file size
    patch_request_class(app, size=None)
    # Specify the endpoint of the login
    login_manager.login_view = 'user.login'

    # You need a login promp
    login_manager.login_message = 'please login first'
    # set session protection level
    # None：forbid session protection
    # 'basic'：base protection
    # 'strong'：The most stringent protection, once the user login information changes, log out immediately
    login_manager.session_protection = 'strong'

