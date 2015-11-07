# Fill in this file and save as settings_local.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = 'ELearning (Return Infinity)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# A tuple that lists people who get code error notifications.
ADMINS = (
    ('Your Name', 'you@example.com'),
)

# Add the name/ip of the server that is running the server
# For development on localhost use this: ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#################################################'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
