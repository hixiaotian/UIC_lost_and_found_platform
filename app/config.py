import os

# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the configuration base class
class Config:
    # key
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'

    # database
    # without warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # auto submit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    POSTS_PER_PAGE = 12

    WTF_CSRF_ENABLED = False

    #the location of the photo uploaded
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/uploads')
    # extra initialize operation
    @staticmethod
    def init_app(app):
        pass


# development environment setting
class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://1730026102:88888888@172.16.199.106/1730026102'

    #if you are localhost, please change to:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flask_lf'


# test environment setting
class TestConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://1730026102:88888888@172.16.199.106/1730026102'
    #if you are localhost, please change to:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flask_lf'


# production environment
class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://1730026102:88888888@172.16.199.106/1730026102'
    #if you are localhost, please change to:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flask_lf'



# dictionary, use string to find corresponding Configuration class
config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

