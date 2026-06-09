from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^3%#cl@iq80hfb8ykeqp&mm^)wril5g-nz2qgoep6#3%=6%on@"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Local dev uses SQLite (see base.py DATABASES). Copy .env.example to .env
# and set DJANGO_SETTINGS_MODULE=cba_site.settings.production to test PostgreSQL.


try:
    from .local import *
except ImportError:
    pass
