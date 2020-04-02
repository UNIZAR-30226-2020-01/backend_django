"""
Django settings for servidor project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Contraseña de la bd en una variable de entorno:
PASSWORD_POSTGRESQL = os.getenv('PASSWORD_POSTGRESQL')

# SECURITY WARNING: don't run with debug turned on in production!


DEPLOYMENT = os.getenv('DEPLOYMENT', None) # Tomamos la variable de entorno del DEPLOYMENT

DEBUG = not DEPLOYMENT # True cuando no est� la var de entorno DEPLOYMENT

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 's7-rest.francecentral.cloudapp.azure.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    ##Autentication
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    # puede que tenga que ir al final:
    'musica',
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

ROOT_URLCONF = 'servidor.urls'

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

WSGI_APPLICATION = 'servidor.wsgi.application'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',  # django-oauth-toolkit < 1.0.0
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Facebook, OpenId, etc)
    ##Ya veremos a ver que hacemos

    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)


# Google configuration
##Hay que conseguir estas cosas de la api de google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')#<your app secret goes here>

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

## Pa mysql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': r'D:\Universidad\Proyecto Software\Django-REST-test\servidor\servidor\mysql.cnf',
#         },
#     }
# }


## postgre no tiene opcion read_default_file, se tiene que poner aqui:
# HOST = postgres://ghjcpmoz:lQ9n_mpqPGxX5TumMLOWA62notw2MmJB@kandula.db.elephantsql.com
# NAME = ghjcpmoz
# database = ghjcpmoz
# port = 5432
# user = ghjcpmoz
# password = lQ9n_mpqPGxX5TumMLOWA62notw2MmJB
# default-character-set = utf8


# Para travis (cuando hace la build travis, pone la variable de entorno TRAVIS=true) y usamos una bd en localhost:
if os.getenv('TRAVIS', None):
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'travis_ci_test',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'CHARSET' : 'utf8',
        }
    }


else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST' : 'kandula.db.elephantsql.com',
            'NAME' : 'ghjcpmoz',
            'DATABASE' : 'ghjcpmoz',
            'PORT' : '5432',
            'USER' : 'ghjcpmoz',
            'PASSWORD' : PASSWORD_POSTGRESQL,
            'CHARSET' : 'utf8',
        },
    }



 #'mysql.cnf',

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


# lo siguiente basado en: https://scotch.io/tutorials/working-with-django-templates-static-files#toc-settings-for-managing-static-files

# Esto indica a django que debe incluir los ficheros est�ticos de la carpeta /servidor/static, aunque no est�n
# incluidos en ninguna app.
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'nuestros_static'),
)

# Esto es solo para producci�n, indica a django d�nde copiar los est�ticos al hacer collectstatic
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
