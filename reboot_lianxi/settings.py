#coding:utf8

"""
Django settings for reboot_lianxi project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!&ydnp(+=@ym!o48iqrd%x3*y#+(zq+&uo%kd%#ri6p26u512d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashborad',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'reboot_lianxi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'reboot_lianxi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "loggers": {
        "opsweb": {
            "level": "DEBUG",
            "handlers": ["console_handle", "opsweb_file_handle","mail"],
        },
        "django": {
            "level": "DEBUG",
            "handlers": [ "django_handle"],
        },


    },
    "handlers":{
        "console_handle": {
            "class": "logging.StreamHandler",
            "formatter": 'simple'
        },
        "opsweb_file_handle": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "opsweb.log"),
            "formatter": "opsweb"
        },
        "django_handle": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "formatter": "opsweb"
        },
        'mail':{
            'class': 'logging.handlers.SMTPHandler',
            'level': 'ERROR',
            'formatter':'opsweb',
            "mailhost": ('smtp.163.com',25),
            "fromaddr":'773437664@qq.com',   ##发件人email
            "toaddrs":['773437664@qq.com'],  ##收件人email
            "subject":"devpos mail",     ##邮件标题
            "credentials":('773437664','feng15961053857')  ##发件人的用户名与密码
        }
    },

    "formatters": {
        "opsweb": {
            "format": "%(asctime)s - %(pathname)s:%(lineno)d[%(levelname)s] - %(message)s"
        },
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    },

    # "root": {
    #     "level": "DEBUG",
    #     "handles": ["console_handle"],
    # }
}

##错误页面跳转
ERROR_TEMPLATE = 'public/error.html'

##登陆url
LOGIN_URL = '/user/login/'


###没有权限url
PERMISSION = '/permission/none'