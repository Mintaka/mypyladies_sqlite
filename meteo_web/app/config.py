
class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/mydata.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # deaktivace funkce Flask-SQLAlchemy - signalizace změn v databázi
