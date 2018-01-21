# UPLOAD_FOLDER = '/public/DATA'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls', 'json'}

COLOURS = ["#1f77b4", "#98df8a", "#8c564b", "#c7c7c7", "#aec7e8", "#d62728",
           "#c49c94", "#bcbd22", "#ff7f0e", "#ff9896", "#e377c2", "#dbdb8d",
           "#ffbb78", "#9467bd", "#f7b6d2", "#17becf", "#2ca02c", "#c5b0d5",
           "#7f7f7f", "#9edae5"]

BACKEND_URL = ""


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    # UPLOAD_FOLDER = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    COLOURS = COLOURS
    BACKEND_URL = BACKEND_URL


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'you-will-never-guess'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
