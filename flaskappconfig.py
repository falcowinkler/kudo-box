import os


class FlaskAppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
