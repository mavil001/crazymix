"""
Django settings for projet_web_app project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import mongoengine
from pathlib import Path

from mongoengine import connect, disconnect
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-is6u851l+p$6in7((wg9^32p#n%=ts#v_d9+mjfoqnh673=#(4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mongoengine',
    'django_mongoengine.mongo_auth',
    'django_mongoengine.mongo_admin',
    'crazymix'

]
                 # + ["django_mongoengine"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet_web_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
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

WSGI_APPLICATION = 'projet_web_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# mongoengine.connect(host='mongodb://crazymix:12345qwe!@localhost:27017/?authMechanism=DEFAULT&authSource=projet_web')
# mongoengine.connect(db='projet_web', host='mongodb://crazymix:12345qwe!@localhost:27017/?authMechanism=DEFAULT&authSource=projet_web', username='crazymix', password='12345qwe!')
mongoengine.connect(db="projet_web", host='mongodb://localhost:27017')

AUTHENTICATION_BACKENDS = (
    # 'mongoengine.django.auth.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'django_mongoengine.mongo_auth.backends.MongoEngineBackend'
)
# SESSION_ENGINE='django_mongoengine.sessions'
# SESSION_SERIALIZER='django_mongoengine.sessions.BSONSerializer'
# AUTH_USER_MODEL='crazymix.User'
# MONGOENGINE_USER_DOCUMENT='django_mongoengine.mongo_auth.models.User'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES={
#     'default': {
#         'ENGINE': 'django.db.backends.dummy',
#     }
# }
disconnect()
MONGODB_DATABASES = {
    'default': {
        # 'ENGINE': 'django_mongoengine',
        'name': 'projet_web',
        'host': 'localhost',
        'port': 27017,
        'tz_aware': True,
    }
}
# connect(
#     db=MONGODB_DATABASES['default']['name'],
#     host=MONGODB_DATABASES['default']['host'],
#     port=MONGODB_DATABASES['default']['port'],
#     username=MONGODB_DATABASES['default']['username'],
#     password=MONGODB_DATABASES['default']['password'],
#     authentication_source=MONGODB_DATABASES['default']['authentication_source']
# )

# MongoClient=('mongodb://marieouiza:projetweb@@localhost:27017/projet_web')
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# AUTH_USER_MODEL = 'mongo_auth.MongoUser'
# MONGOENGINE_USER_DOCUMENT = 'crazymix.User'
LOGIN_REDIRECT_URL= '/crazymix'

# AUTHENTICATION_BACKENDS = (
# 'mongoengine.django.auth.MongoEngineBackend',
# )
#
# SESSION_ENGINE = 'mongoengine.django.sessions'