class Config:
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = f'sqlite:///./sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    from my_utils.settings import get_settings
    hostname = get_settings('Database', 'hostname')
    username = get_settings('Database', 'username')
    password = get_settings('Database', 'password')
    db_name = get_settings('Database', 'db')
    SQLALCHEMY_DATABASE_URI = f'mysql://{username}:{password}@{hostname}/{db_name}'
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
