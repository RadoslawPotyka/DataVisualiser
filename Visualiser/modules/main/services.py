from .models import User


class WorkingContextService(object):
    """
    Service handling, controlling and interacting with the context of the application.
    """

    @staticmethod
    def get_user_logged_in():
        user = User(name="guest")

        return user
