class Config(object):
    TESTING = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
