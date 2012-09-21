#!/usr/bin/env python

# http://flask.pocoo.org/docs/config/#development-production

class Config(object):
    SECRET_KEY = 'ww+nka=g+ihmn#bnmslp_k0xr%wj9$oezlzm3pxcni@yos99f#'
    SITE_NAME = 'ontotest'
    MEMCACHED_SERVERS = ['localhost:11211']
    SYS_ADMINS = ['foo@example.com']

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestConfig(Config):
    DEBUG = False
    TESTING = True

class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    TESTING = True

