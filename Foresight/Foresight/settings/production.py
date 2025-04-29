from .base import *

DEBUG = False
ALLOWED_HOSTS = [host.strip() for host in os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': int(os.getenv('MYSQL_PORT', '3306')),  # ðŸ‘ˆ important fix
    }
}

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True  # keep False until SSL working
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

