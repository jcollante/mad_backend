import os

base_dir = os.path.abspath(os.getcwd())

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('app-secret')
    # other generic configuration
    # ..options

class DevConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    DATABASE = 'pandas'
    DATABASE_NAME = 'AIS_2022_03_12.csv'
    SQLALCHEMY_DATABASE_URI = f""

class StgConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    DATABASE = 'sqlite'
    DATABASE_NAME = 'vessels.sqlite'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_dir}/{DATABASE_NAME}"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    FLASK_ENV = 'production'
    DATABASE = 'postgresql'

_config = {
    'default': DevConfig,
    'development': DevConfig,
    'production': ProdConfig
}