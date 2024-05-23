"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# 静的ファイルの設定
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#ローカル環境
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # プロジェクトディレクトリ内の'staticfiles'ディレクトリを指定
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 'testApp/static'ディレクトリを静的ファイルのソースとして追加
]

# # 本番環境設定
# DEBUG = os.getenv('DEBUG') == 'True'
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
# STATIC_ROOT = os.getenv('STATIC_ROOT')
# MEDIA_ROOT = os.getenv('MEDIA_ROOT')



# Application definition

INSTALLED_APPS = [
    'social_django',
    'booking.apps.BookingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    #'testApp',
    'rest_framework'
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Djangoのデフォルトの認証バックエンド
    'social_core.backends.line.LineOAuth2',  # LINEのOAuth2認証バックエンド
]
 

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'booking/templates')],
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

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

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
LOGIN_REDIRECT_URL = 'booking:store_list' # ログイン後にリダイレクトするURL
LOGOUT_REDIRECT_URL = 'booking:login' 
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

LINE_CHANNEL_ID = os.getenv('LINE_CHANNEL_ID')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_REDIRECT_URL = os.getenv('LINE_REDIRECT_URL')
PAYMENT_API_KEY = os.getenv('PAYMENT_API_KEY')
LINE_ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
user_id = os.getenv('user_id')
CELERY_broker_url = os.getenv('CELERY_broker_url')
PAYMENT_API_URL = os.getenv('PAYMENT_API_URL')
WEBHOOK_URL_BASE = os.getenv('WEBHOOK_URL_BASE')
CANCEL_URL = os.getenv('CANCEL_URL')
