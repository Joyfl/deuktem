# -*- coding: utf-8 -*-
"""
    deuktem.config
    ~~~~~~~~~~~~~~

    This module provides configurations. Secret data is stored in `secret`
    module.

    :secret.DATABASE_PASSWORD: A password for database.
    :secret.RABBITMQ_PASSWORD: A password for RabbitMQ.
    :secret.SECRET_KEY: A secret key.
"""

from . import secret


class DefaultConfig(object):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://'\
                              'deuktem:%s@localhost/deuktem'\
                              '?sslmode=disable' % secret.DATABASE_PASSWORD
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    BROKER_URL = 'amqp://deuktem:%s@localhost:5672/deuktem' % (
        secret.RABBITMQ_PASSWORD
    )

    SECRET_KEY = secret.SECRET_KEY
    SERVER_NAME = 'deuktem.joyfl.net'
    DEBUG = False

    ALLOWED_FACEBOOK_USERS = [
        '100000888155228',  # 전수열
        '100001724518360',  # 설진석
        '100001647609513',  # 진재규
        '100001275667385',  # 길형진
    ]

    PHOTO_MAX_RESOLUTION = 320


class TestConfig(DefaultConfig):

    TESTING = True
