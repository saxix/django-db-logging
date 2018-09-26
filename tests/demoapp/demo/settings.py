from django_db_logging.router import LoggingRouter

DEBUG = True
STATIC_URL = '/static/'

SITE_ID = 1
ROOT_URLCONF = 'demo.urls'
SECRET_KEY = 'abc'
STATIC_ROOT = 'static'
MEDIA_ROOT = 'media'

INSTALLED_APPS = ['django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.admin',
                  'admin_extra_urls',
                  'django_db_logging',
                  'demo'
                  ]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': ['django.contrib.messages.context_processors.messages',
                                   'django.contrib.auth.context_processors.auth',
                                   "django.template.context_processors.request",
                                   ]
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'debug': {
            'format': '%(levelno)s:%(levelname)-8s %(name)s %(funcName)s:%(lineno)s:: %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        },
        'db': {
            'level': 'DEBUG',
            'class': 'django_db_logging.handlers.DBHandler',
        },
        'db-demo': {
            'level': 'DEBUG',
            'class': 'django_db_logging.handlers.DBHandler',
            'model': 'demo.CustomLogger',
        },
    },
    'loggers': {
        'django_db_logging': {
            'handlers': ['null', 'db'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'demo': {
            'handlers': ['db-demo'],
            'propagate': True,
            'level': 'DEBUG'
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

DATABASE_ROUTERS = [
    LoggingRouter("logging")
]
