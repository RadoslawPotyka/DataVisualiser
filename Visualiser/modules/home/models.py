class TemplateResourcesData(object):
    """
    Object representation of template metadata for inclusion in the template file. Contains lists of html, css and html
    strings which can be embedded in a template file embedding.

    Attributes:
        @property css_list(list(str)): list of string containing links to css stylesheets.
        @property js_list(list(str)): list of strings containing script to include in a html page.
        @property html_list(list(str)): list of stringified html files to include in an html page.
    """

    def __init__(self):
        self.__css_list = []
        self.__js_list = []
        self.__html_list = []

    @property
    def css_list(self):
        return self.__css_list

    @css_list.setter
    def css_list(self, css):
        self.__css_list = css

    @property
    def js_list(self):
        return self.__js_list

    @js_list.setter
    def js_list(self, js):
        self.__js_list = js

    @property
    def html_list(self):
        return self.__html_list

    @html_list.setter
    def html_list(self, html):
        self.__html_list = html


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
