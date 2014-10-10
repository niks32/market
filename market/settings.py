import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=(js6at(yrn52uefh7brmwzb$f2f(jjjt-0@$2!4^ped3!&=09'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'market', 'static')
]

#капча
CAPTCHA_OUTPUT_FORMAT = ' <div class="col-lg-6">  %(hidden_field)s %(text_field)s </div> <div class="col-lg-6"> %(image)s </div>'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]


TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'templates')
]

TEMPLATE_CONTEXT_PROCESSORS = [
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request",
"saleor.core.context_processors.default_currency",

"django.core.context_processors.csrf",

]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # TODO: this one is slow, but for now need for mptt?
    'django.template.loaders.eggs.Loader'
]

# Application definition
INSTALLED_APPS = (

    # Django modules

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Temporary
    'django.contrib.webdesign',

    # Local apps
    'market.cart',
    'market.core',
    'market.registration',
    'market.accounts',
    'market.product',

    # External apps
    'south',
    'babeldjango'
    'debug_toolbar',
    'captcha',
    'any_imagefield',
    'mptt',
)

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware'
    'babeldjango.middleware.LocateMiddleware'
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'market.cart.middleware.CartMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'market.registration.backends.EmailPasswordBackend',
    #'market.registration.backends.TrivialBackend',
)

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

ROOT_URLCONF = 'market.urls'

WSGI_APPLICATION = 'market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

DEFAULT_CURRENCY = 'USD'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOGIN_REDIRECT_URL = 'home'