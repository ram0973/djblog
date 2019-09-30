"""
Django settings for core project.
https://docs.djangoproject.com/en/2.0/topics/settings/
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
import time
import raven
from django.utils.translation import gettext_lazy as _
from configurations import Configuration, values
from dotenv import load_dotenv

load_dotenv()


class Common(Configuration):
    """ common settings """
    AUTH_USER_MODEL = 'accounts.User'

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    CORE_DIR = os.path.join(BASE_DIR, 'core')
    PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
    STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
    ASSETS_ROOT = os.path.join(PUBLIC_DIR, 'assets')
    MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
    STATICFILES_DIRS = (
        os.path.join(PUBLIC_DIR, 'assets'),
    )

    STATIC_URL = '/static/'
    ASSETS_URL = '/assets/'
    MEDIA_URL = '/media/'
    UPLOADS_URL = '/uploads/'

    # See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
    SECRET_KEY = values.SecretValue()

    INTERNAL_IPS = ['127.0.0.1', ]

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django.contrib.admindocs',
        'django_extensions',
        'martor',

        'core',
        'accounts.apps.AccountsConfig',
        'blog.apps.BlogConfig',
        'photos.apps.PhotosConfig',
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

    ROOT_URLCONF = 'core.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(CORE_DIR, 'templates')],
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

    WSGI_APPLICATION = 'core.wsgi.application'

    # https://docs.djangoproject.com/en/2.0/ref/settings/#databases
    DATABASES = values.DatabaseURLValue()
    # 'postgresql://postgres:postgres@localhost/core')
    # 'sqlite:///core.sqlite3'

    # https://docs.djangoproject.com/en/2.0/ref/settings/
    # #auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.'
                    'NumericPasswordValidator',
        },
    ]

    # https://docs.djangoproject.com/en/2.0/topics/i18n/

    LANGUAGE_CODE = 'ru-RU'

    LANGUAGES = [
        ('ru', _('Russian')),
        ('en', _('English')),
    ]

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/

    MARTOR_ENABLE_LABEL = True
    MARTOR_UPLOAD_PATH = 'uploads/images/{}'.format(time.strftime('%Y/%m/%d/'))
    MAX_IMAGE_UPLOAD_SIZE = 5242880  # 5MB
    MARTOR_UPLOAD_URL = '/api/uploader/'

    MARTOR_ENABLE_CONFIGS = {
        'imgur': 'true',  # to enable/disable imgur/custom uploader.
        'mention': 'false',  # to enable/disable mention
        'jquery': 'true',  # to include/revoke jquery
                           # (require for admin default django)
        'living': 'false',  # to enable/disable live updates in preview
    }


class Dev(Common):
    """ development settings """
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    TEMPLATE_DEBUG = True


class Staging(Common):
    """ staging settings """
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    DEBUG = False
    TEMPLATE_DEBUG = False
    # RAVEN_CONFIG = copy.deepcopy(Common.RAVEN_CONFIG)
    # RAVEN_CONFIG['environment'] = 'staging'


class Prod(Common):
    """ production settings """
    ALLOWED_HOSTS = [values.Value(environ_name='DOMAIN'), ]
    DEBUG = False
    TEMPLATE_DEBUG = False
    # RAVEN_CONFIG = copy.deepcopy(Common.RAVEN_CONFIG)
    # RAVEN_CONFIG['environment'] = 'prod'
    RAVEN_CONFIG = {
        'dsn': values.Value(environ_name='SENTRY_DSN'),
        'release': raven.fetch_git_sha(Common.BASE_DIR),
        'environment': 'Prod',
        'ignore_urls': ['http://localhost/', '127.0.0.1']
    }
    INSTALLED_APPS = Common.INSTALLED_APPS + \
        ['raven.contrib.django.raven_compat']
    MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.'
                  'Sentry404CatchMiddleware'] + Common.MIDDLEWARE
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',  # or ERROR, WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.'
                         'SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }
