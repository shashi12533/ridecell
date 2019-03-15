# -*- coding: utf-8 -*-

from datetime import timedelta
from os import environ, path
from sys import modules

__author__ = 'shashi'

pwd = path.dirname(path.abspath(__file__))


class BaseConfig(object):
    # Flask #
    FLASK_APP_NAME = "ridecell"
    FLASK_DEBUG = True
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_CYCLE = 3600
    SQLALCHEMY_CONVERT_UNICODE = True

class ShashiDevConfig(BaseConfig):
     sham = "dhdhebh"

   
    
        



config = None


def get_config(cache=True):
    global config
    if cache and config:
        return config
   
    # env = environ.get('ONEHOP_ENV')
    env = 'ShashiDev'
    if not env:
        raise Exception('Config environment not defined.')

    # module object for this file viz. config.py
    module_object = modules[__name__]
    class_name = '{0}Config'.format(env)

    # get class object
    conf = getattr(module_object, class_name)
    conf.config_in_use = class_name
    config = conf
    return conf
