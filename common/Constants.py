import os

class Constants(object):
    botToken = os.environ['BOT_TOKEN']

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
        return cls.instance
