class TemplateResourcesData(object):
    """
    Object representation of template metadata for inclusion in the template file. Contains lists of html, css and html
    strings which can be embedded in a template file embedding.

    Attributes:
        @property css(str): list of string containing links to css stylesheets.
        @property js(str): list of strings containing script to include in a html page.
        @property html(str): list of stringified html files to include in an html page.
    """

    def __init__(self):
        self.__css = []
        self.__js = []
        self.__html = []

    @property
    def css(self):
        return self.__css

    @css.setter
    def css(self, css):
        self.__css = css

    @property
    def js(self):
        return self.__js

    @js.setter
    def js(self, js):
        self.__js = js

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, html):
        self.__html = html


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
