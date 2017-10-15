from Visualiser.modules.main.models import User


class HomeController(object):
    def __init__(self, user=None):
        if user is None:
            user = User(name="guest")

        self.__user_logged_in = user

    @property
    def user_logged_in(self):
        return self.__user_logged_in
