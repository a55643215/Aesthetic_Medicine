import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://doctordb:X1rooPEa77V2nfQlhH5OwwzVlx6WNt9n@dpg-cjbikn45kgrc73a7of9g-a.singapore-postgres.render.com/doctordb'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')