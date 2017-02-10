# -*- coding: utf-8 -*-

import os
# import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TOKEN = '520a69e999343680d4ae35ead9c877418bd37510:r8xYTTOPfMFUpxLqbALEFxJwHfI=' \
            ':eyJkZWFkbGluZSI6MTQ4NTQwMjE0OCwiYWN0aW9uIjoiZ2V0IiwidWlkIjoiNTY3NTkxIiw' \
            'iYWlkIjoiMTI1MzA4NCIsImZyb20iOiJmaWxlIn0='
    FANXIANGCE_MAIL_SUBJECT_PREFIX = u'[翻相册]'
    FANXIANGCE_MAIL_SENDER = 'mimi_19@sina.com'
    FANXIANGCE_ADMIN = 'withlihui@gmail.com' # os.environ.get('FANXIANG_ADMIN')
    UPLOADED_PHOTOS_DEST = os.getcwd() + '/app/static/img/'  # local test
    FANXIANGCE_COMMENTS_PER_PAGE = 15
    FANXIANGCE_ALBUMS_PER_PAGE = 12
    FANXIANGCE_PHOTOS_PER_PAGE = 20
    FANXIANGCE_ALBUM_LIKES_PER_PAGE = 12
    FANXIANGCE_PHOTO_LIKES_PER_PAGE = 20
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mimi_19@sina.com' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'december' #os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class HerokuConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mimi_19@sina.com'  # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'december'  # os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']



config = {
    'development' : DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}