"""
Django settings for bboa2 project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'FAKE_VALUE_REAL_VALUE_SET_FROM_CUSTOM_SETTINGS.PY'
# I recommend setting a default/false value here
# and then overwriting in local/custom settings.
# This keeps the app functional if anyone clones the repository
# You can generate a new SECRET_KEY using tools such as
# http://www.miniwebtool.com/django-secret-key-generator/

SETTINGS_MODE = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_start.settings.base")
SETTINGS_MODE = SETTINGS_MODE.upper().split('.')
SETTINGS_MODE = SETTINGS_MODE[-1]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Update Allowed Hosts to control access more closely.
ALLOWED_HOSTS = ['*']

# Set ADMINS and MANAGERS in your custom settings file. eg. local.py
ADMINS = (
     ('Alan Viars', 'aviars@videntity.com'),
    ('Mark Scrimshire', 'mark@ekivemark.com'),
)
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #1st Party (in-house) -----------
    'apps.accounts', # Account related services
    'apps.capabilities', # Define scopes and related protected resource URLs.
    'apps.dot_ext', # Custom extensions to DOT 
    'apps.home', # Landing pages, etc.
    'apps.education',
    # 'apps.fhir',
    'apps.fhir.core',
    'apps.fhir.server',
    'apps.fhir.bluebutton',
   
    #3rd Party ---------------------
    'corsheaders',
    'bootstrapform',
    
     # DOT must be installed after apps.dot_ext in order to override templates
    'oauth2_provider',
    
]

# CorsMiddleware needs to come before Django's CommonMiddleware if you are using Django's
# USE_ETAGS = True setting,
# otherwise the CORS headers will be lost from the 304 not-modified responses,
# causing errors in some browsers.
# See https://github.com/ottoyiu/django-cors-headers for more information.
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = '_start.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..','templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = '_start.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME':     os.environ.get('DATABASE_NAME', os.path.join(BASE_DIR, '..',   'db.sqlite3')),
        'USER':     os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST':     os.environ.get('DATABASE_HOST', ''),
        'PORT':     os.environ.get('DATABASE_PORT', ''),
    
    }
}

#This helps Django messages format nicely with Bootstrap3. -AV
MESSAGE_TAGS ={ messages.DEBUG:   'debug',
                messages.INFO:    'info',
                messages.SUCCESS: 'success',
                messages.WARNING: 'warning',
                messages.ERROR:   'danger'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'collectedstatic')
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'sitestatic'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS =[
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s [%(process)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'hhs_server': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'oauth2_provider': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'tests': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }

    },
}

#Email Sending Opts
AWS_ACCESS_KEY_ID     = os.environ.get('AWS_ACCESS_KEY_ID', 'your-key-here')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'your-secret-here')
HOSTNAME_URL          = os.environ.get('HOSTNAME_URL', 'http://127.0.0.1:8000')
SEND_EMAIL            = True
ORGANIZATION_NAME = os.environ.get('ORGANIZATION_NAME', 'CMS OAuth2 Server')
EMAIL_BACKEND = 'django_ses.SESBackend'
SIGNUP_TIMEOUT_DAYS = 3
EMAIL_HOST_USER = 'sales@videntity.com'
INVITE_REQUEST_ADMIN = 'sales@videntity.com'

MIN_PASSWORD_LEN = 8
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'apps.accounts.auth.SettingsBackend',
            
            )

OAUTH2_PROVIDER_APPLICATION_MODEL='dot_ext.Application'
OAUTH2_PROVIDER = {
    'OAUTH2_VALIDATOR_CLASS': 'apps.dot_ext.oauth2_validators.SingleAccessTokenValidator',
    'OAUTH2_SERVER_CLASS': 'apps.dot_ext.oauth2_server.Server',
    'SCOPES_BACKEND_CLASS': 'apps.dot_ext.scopes.CapabilitiesScopes',
}

# These choices will be available in the expires_in field
# of the oauth2 authorization page.
DOT_EXPIRES_IN = (
    (86400, _("1 Day")),
    (86400*7, _("1 Week")),
    (86400*365, _("1 Year")),
    (86400*365*100, _("Forever")),
)


THEMES = {"0": {'NAME': "Default-Readable",
                'PATH':"theme/default/",
                'INFO': "Readable san-serif base theme"},

          "3": {'NAME': "Readable",
                'PATH': "theme/readable/",
                'INFO': "Easy to read Bootswatch Theme"},
          "4": {'NAME': "Cerulean",
                'PATH': "theme/cerulean/",
                'INFO': "Blue Bootswatch theme theme"},
          "5": {'NAME': "Cosmo",
                'PATH': "theme/cosmo/",
                'INFO': "Cosmo bootswatch theme"},
          "6": {'NAME': "Cyborg",
                'PATH': "theme/cyborg/",
                'INFO': "Cyborg bootswatch theme"},
          "7": {'NAME': "Darkly",
                'PATH': "theme/darkly/",
                'INFO': "Darkly bootswatch theme"},
          "8": {'NAME': "Flatly",
                'PATH': "theme/flatly/",
                'INFO': "Flatly bootswatch theme"},
          "9": {'NAME': "Journal",
                'PATH': "theme/journal/",
                'INFO': "Journal bootswatch theme"},
          "10":{'NAME': "Lumen",
                'PATH': "theme/lumen/",
                'INFO': "Lumen bootswatch theme"},
          "11": {'NAME': "Paper",
                 'PATH': "theme/paper/",
                 'INFO': "Paper bootswatch theme"},
          "12": {'NAME': "Sandstone",
                 'PATH': "theme/sandstone/",
                 'INFO': "Sandstone bootswatch theme"},
          "13": {'NAME': "Simplex",
                 'PATH': "theme/simplex/",
                 'INFO': "Simplex bootswatch theme"},
          "14": {'NAME': "Slate",
                 'PATH': "theme/slate/",
                 'INFO': "Slate bootswatch theme"},
          "15": {'NAME': "Spacelab",
                 'PATH': "theme/spacelab/",
                 'INFO': "Spacelab bootswatch theme"},
          "16": {'NAME': "Superhero",
                 'PATH': "theme/superhero/",
                 'INFO': "Superhero bootswatch theme"},
          "17": {'NAME': "United",
                 'PATH': "theme/united/",
                 'INFO': "United bootswatch theme"},
          "18": {'NAME': "Yeti",
                 'PATH': "theme/yeti/",
                 'INFO': "Yeti bootswatch theme"},
          "SELECTED": "0"}

if THEMES['SELECTED'] not in THEMES:
    THEME_SELECTED = "0"
else:
    THEME_SELECTED = THEMES["SELECTED"]

THEME = THEMES[THEME_SELECTED]

APPLICATION_TITLE = "CMS OAuth2 Server"

# Set the default Encoding standard. typically 'utf-8'
ENCODING = 'utf-8'

SETTINGS_EXPORT = [
    'DEBUG',
    'APPLICATION_TITLE',
    'THEME',
    'STATIC_URL',
    'SETTINGS_MODE',
]

#Stub for Custom Authentication Backend (This will change/be removed..just framing)

SLS_USER       = "ben"
SLS_PASSWORD   = "pbkdf2_sha256$24000$V6XjGqYYNGY7$13tFC13aaTohxBgP2W3glTBz6PSbQN4l6HmUtxQrUys="
SLS_FIRST_NAME = "Ben"
SLS_LAST_NAME  = "Barker"
SLS_EMAIL      = "ben@example.com"

# try:
#     from .local import *
# except:
#     pass
#
