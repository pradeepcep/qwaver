"""
Django settings for qwaver project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from configparser import RawConfigParser

# loading settings.ini
import pymysql

config = RawConfigParser()
settings_folder = os.path.dirname(os.path.abspath(__file__))
ini_file = os.path.join(settings_folder, 'settings.ini')
# dummy settings; these will be replaced when loading 'settings.ini'
config['config'] = {
    'ENVIRONMENT': 'local',
    'SECRET_KEY': '**************************************************',
    'DATABASE_ENGINE': '[your database ENGINE]',
    'DATABASE_NAME': '[your database name]',
    'DATABASE_USER': '[your database user]',
    'DATABASE_PASS': '[the database password for that user]',
    'DATABASE_HOST': '[the database host url]',
    'DATABASE_PORT': '[the database connection port]',
    'DATABASE_CONN_MAX_AGE': '0',
    'DEBUG': 'True',
    'EMAIL_HOST': 'xxxxxxxxxx',
    'EMAIL_PORT': '0',
    'EMAIL_USE_TLS': 'True',
    'EMAIL_HOST_USER': 'xxxxxxxxxx',
    'EMAIL_HOST_PASSWORD': 'xxxxxxxxxx',
    'MAX_TABLE_ROWS': '500',
}
config.read(ini_file)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('config', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get('config', 'DEBUG') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'queries.apps.QueriesConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qwaver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qwaver.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if config.get('config', 'ENVIRONMENT').lower() == 'prod':
    DATABASES = {
        'default': {
            'ENGINE': config.get('config', 'DATABASE_ENGINE'),
            'NAME': config.get('config', 'DATABASE_NAME'),
            'USER': config.get('config', 'DATABASE_USER'),
            'PASSWORD': config.get('config', 'DATABASE_PASS'),
            'HOST': config.get('config', 'DATABASE_HOST'),
            'PORT': config.get('config', 'DATABASE_PORT'),
            'CONN_MAX_AGE': None,
            'OPTIONS': {
                # 'sslmode': 'require'
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# TODO make conditional if using MySQL
# Fake PyMySQL's version and install as MySQLdb
# https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/
pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'queries-home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('config', 'EMAIL_HOST')
EMAIL_PORT = int(config.get('config', 'EMAIL_PORT'))
EMAIL_USE_TLS = config.get('config', 'EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = config.get('config', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('config', 'EMAIL_HOST_PASSWORD')

ADMINS = [('Brian', 'geneffects@gmail.com')]
SERVER_EMAIL = 'server@qwaver.io'

MAX_TABLE_ROWS = int(config.get('config', 'MAX_TABLE_ROWS'))

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/home/geneffec/qwaver/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
