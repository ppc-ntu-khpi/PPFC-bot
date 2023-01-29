class Constants(object):
    botToken: str = "5934033684:AAGdydIavf-U0TMK7qGjI2xpGO4y1saTDlM"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Constants, cls).__new__(cls)
        return cls.instance