#-----------------------------------------
#-  Copyright (c) 2023. Lazovikov Illia  -
#-----------------------------------------

import os

class Constants(object):
   
    botToken = os.environ['BOT_TOKEN']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    baseLink = os.environ['BASE_LINK']
    restart = os.environ["HARD_RESTART"]
    version ="(v0.9.5)"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
        return cls.instance
