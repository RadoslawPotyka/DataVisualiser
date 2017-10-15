class User(object):
    def __init__(self, name=None, login=None):
        self.__name = name
        self.__login = login

    @property
    def name(self):
        return self.__name

    @property
    def login(self):
        return self.__login
