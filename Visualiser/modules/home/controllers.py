from ..common.services import WorkingContextService


class HomeController(object):
    """
    Base view controller. Class is responsible for controlling all base functionalities that each controller
    needs or might need to have in order to properly control application's behaviour, visible elements and actions
    that are available for user.

    """

    @property
    def user_logged_in(self):
        return WorkingContextService.get_user_logged_in()
