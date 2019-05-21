"""
Django settings for ConnectID project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

with open(os.path.join(BASE_DIR, 'secrets.yml'), 'r') as yamlfile:
    yamlconfig = yaml.load(yamlfile)
    DEBUG = yamlconfig['debug']
    SECRET_KEY = yamlconfig['secretKey']
    ALLOWED_HOSTS = yamlconfig['allowedHosts']
    PRODUCTION_STATIC_ROOT_PATH = yamlconfig['productionStaticRoot']
    PRODUCTION_MEDIA_ROOT_PATH = yamlconfig['productionMediaRoot']
    SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = yamlconfig['linkedinKey']
    SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = yamlconfig['linkedinSecret']

INTERNAL_IPS = (
    '127.0.0.1',
)

# Setting up the server to send automated emails from
from .email_info import EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_SSL = EMAIL_USE_SSL

# This is where the log emails go to
ADMINS = [("ConnectID_admin", EMAIL_HOST_USER), ]

# Application definition

INSTALLED_APPS = [
    'home.apps.HomeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',  # https://django-compressor.readthedocs.io/en/latest/settings/#settings
    'rules.apps.AutodiscoverRulesConfig',  # https://github.com/dfunckt/django-rules
    'chat',
    'tellme',
    'widget_tweaks',
    'social_django',
    'watson',
    'django_cleanup',
    'bugsnag',
    'django_jenkins'

]

TELLME_FEEDBACK_EMAIL = EMAIL_HOST_USER

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bugsnag.django.middleware.BugsnagMiddleware',
]

# for libsass compiler
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# django social auth
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'public-profile-url', 'picture-urls::(original)', 'picture-url']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                          ('firstName', 'first_name'),
                                          ('lastName', 'last_name'),
                                          ('emailAddress', 'email_address'),
                                          ('pictureOriginal', 'picture-urls::(original)'), # When these start working, you can use this in the edit_profile_picture.html
                                          ('profileURL', 'public-profile-url'),
                                          ('picture-url', 'picture-url'),
                                          ('headline', 'headline'),
                                          ]
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# Notice 'associate_by_email' is enabled (this is not by default). To make sure no new user is created when the linkedin app is changed for example
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'home.social_auth_extra_functions.save_extra_data',
)

# for django-rules
AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',  # for django-rules
    'social_core.backends.linkedin.LinkedinOAuth2', # Social_django social django socialdjango
    'django.contrib.auth.backends.ModelBackend',  # to login with username/password
)

ROOT_URLCONF = 'ConnectID.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'home', 'templates')]
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

WSGI_APPLICATION = 'ConnectID.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if DEBUG:
    DATABASENAME = "developdb.sqlite3"
else:
    DATABASENAME = "db.sqlite3"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, DATABASENAME),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# https://scotch.io/tutorials/working-with-django-templates-static-files
STATIC_URL = '/static/' # leave this, it is the name in this three: ConnectID/home/static/home/...
MEDIA_URL = '/media/' # leave this, it is the name in this three: ConnectID/home/media/home/...

if DEBUG:  # ABSOLUTE PATH TO STATIC AND MEDIA FILES (should be /var/html/www/static etc in production)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticRootDEBUG_DEVELOP")
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediaRootDEBUG_DEVELOP')
else:
    STATIC_ROOT = PRODUCTION_STATIC_ROOT_PATH
    MEDIA_ROOT = PRODUCTION_MEDIA_ROOT_PATH

STATICFILES_FINDERS = [
    'compressor.finders.CompressorFinder',
    "django.contrib.staticfiles.finders.FileSystemFinder",
    # heel belangrijk om deze twee toe te voegen! Dit zijn de defaults, maar worden overschreven door STAITCFILES_FINDERS te defigneren
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
    # heel belangrijk om deze twee toe te voegen! Dit zijn de defaults, maar worden overschreven door STAITCFILES_FINDERS te defigneren
]
'''
STATICFILES_DIRS = (
    PRODUCTION_STATIC_ROOT_PATH
)
'''

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/loginSuccess'

# TODO https://docs.djangoproject.com/en/2.0/topics/email/
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BUGSNAG = {
    'api_key': 'b933184587896544b7c0794f0d8bff09'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'level': 'ERROR',
        'handlers': ['bugsnag'],
    },

    'handlers': {
        'bugsnag': {
            'level': 'INFO',
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
    }
}

# for django_jenkins config, was an example but when uncommented some don't work
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
 #   'django_jenkins.tasks.run_pylint',
 #   'django_jenkins.tasks.run_jslint',
 #   'django_jenkins.tasks.run_csslint',
 #   'django_jenkins.tasks.run_sloccount'
)


#TODO below is for heroku together with the whitenoise line in middleware


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
PROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT  =   os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


import dj_database_url
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)