# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    LOG_MAIL_SUBJIECT_PRIFIX = '[log]'
    LOG_MAIL_SENDER = 'Li Hui<lihui@log.com>'
    LOG_ADMIN = os.environ.get('LOG_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development' : DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

