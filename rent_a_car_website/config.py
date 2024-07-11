import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    LANGUAGES = ['en', 'no', 'ru']
