import os

class Constants(object):
    botToken = os.environ['BOT_TOKEN']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    baseLink = os.environ['BASE_LINK']
    
    version ="(v0.9.3)"

    restart = os.environ["HARD_RESTART"]
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
        return cls.instance
