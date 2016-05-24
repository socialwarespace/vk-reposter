# -- coding: utf-8 --
"""
Django settings for conf project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+i0edg=v1d(0)%x)nf4lg!*ocpt*o8go1#z$(9@h)hjs47cs#r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'reposter',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(
    os.path.dirname(BASE_DIR), 'public', 'static'
)

# Media files (user content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(
    os.path.dirname(BASE_DIR), 'public', 'media'
)


# Celery configuration
# http://docs.celeryproject.org/

BROKER_URL = "redis://localhost:6379/0"

# Расписание выполнения задач (аналог CRON)
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    'parse_posts': {
        'task': 'parse_posts',
        'schedule': crontab(minute='1', hour='*'),
    },
    'repost_posts': {
        'task': 'repost_posts',
        'schedule': crontab(minute='3', hour='*'),
    },
}


# Настройки VK
VK_APP_ID = ''          # ID приложения VK
VK_USER_LOGIN = ''      # Логин пользователя VK
VK_USER_PASSWORD = ''   # Пароль пользователя VK
VK_SCOPE = 'wall'       # права доступа к аккаунту пользователя
# https://new.vk.com/dev/permissions

# Формула рейтинга постов
VK_RATING_FORMULA = 's / ((10 * r + l) / t )'

# Максимальный рейтинг при котором объявление обрабатывается
VK_RATING_LIMIT = 10

# Количество постов запрашиваемое за один запрос (не больше 100)
# https://vk.com/dev/wall.get
VK_POST_COUNT = 100

# Таймаут в секундах при обращениях к VK. Если больше 3 запросов в секунду
# будет ошибка
VK_API_INTERVAL = 1

# Сообщение репоста
VK_REPOST_MESSAGE = u''

# Постить в группу (имя или идентификатор группу)
VK_REPOST_TO = ''


try:
    from conf.settings_local import *
except ImportError:
    pass


if DEBUG:
    INTERNAL_IPS = ('127.0.0.1', )
    DISABLE_PANELS = []

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True
    }

    # additional modules for development
    INSTALLED_APPS += (
        'debug_toolbar',
    )
