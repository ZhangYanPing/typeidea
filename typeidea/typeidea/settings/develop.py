from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqllite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqllite3'),
    }
}
