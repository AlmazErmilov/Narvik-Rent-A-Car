import os

class Config:
    # ASVS 13.3.1: no signing key is embedded in application source.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    LANGUAGES = ['en', 'no', 'ru']
