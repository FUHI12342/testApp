"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&670@la%)g1zo2y7(+4+^pl00sb(cjl4rpvkf@2ly)eo+a$1k!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'booking.apps.BookingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
from dotenv import load_dotenv
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR /'static_local']
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PARENT_DIR = BASE_DIR.parent
#env_path = PARENT_DIR / "auth/.env"
#load_dotenv(env_path)
STATIC_ROOT = PARENT_DIR / "site/public/static"
SECRET_KEY = os.environ.get("secret_key")


import datetime

PUBLIC_HOLIDAYS = [
    # 2020
    datetime.date(year=2020, month=1, day=1),
    datetime.date(year=2020, month=1, day=13),
    datetime.date(year=2020, month=2, day=11),
    datetime.date(year=2020, month=2, day=23),
    datetime.date(year=2020, month=2, day=24),
    datetime.date(year=2020, month=3, day=20),
    datetime.date(year=2020, month=4, day=29),
    datetime.date(year=2020, month=5, day=3),
    datetime.date(year=2020, month=5, day=4),
    datetime.date(year=2020, month=5, day=5),
    datetime.date(year=2020, month=7, day=20),
    datetime.date(year=2020, month=8, day=11),
    datetime.date(year=2020, month=9, day=21),
    datetime.date(year=2020, month=9, day=22),
    datetime.date(year=2020, month=10, day=12),
    datetime.date(year=2020, month=11, day=3),
    datetime.date(year=2020, month=11, day=23),

    # 2021
    datetime.date(year=2021, month=1, day=1),
    datetime.date(year=2021, month=1, day=11),
    datetime.date(year=2021, month=2, day=11),
    datetime.date(year=2021, month=2, day=23),
    datetime.date(year=2021, month=3, day=20),
    datetime.date(year=2021, month=4, day=29),
    datetime.date(year=2021, month=5, day=3),
    datetime.date(year=2021, month=5, day=4),
    datetime.date(year=2021, month=5, day=5),
    datetime.date(year=2021, month=7, day=19),
    datetime.date(year=2021, month=8, day=11),
    datetime.date(year=2021, month=9, day=20),
    datetime.date(year=2021, month=9, day=23),
    datetime.date(year=2021, month=10, day=11),
    datetime.date(year=2021, month=11, day=3),
    datetime.date(year=2021, month=11, day=23),
]

LOGIN_URL = 'booking:login'
LOGIN_REDIRECT_URL = 'booking:store_list'
LOGOUT_REDIRECT_URL = 'booking:login'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'
