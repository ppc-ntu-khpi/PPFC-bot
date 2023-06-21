#-----------------------------------------
#-  Copyright (c) 2023. Lazovikov Illia  -
#-----------------------------------------

import os

class Constants(object):
   
    botToken = os.environ['BOT_TOKEN']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    baseLink = os.environ['BASE_LINK']
    version ="(v1.0.0)"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
        return cls.instance
