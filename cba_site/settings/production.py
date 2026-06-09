from pathlib import Path

import environ

from .base import *

env = environ.Env(
    DEBUG=(bool, False),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
)

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://cbaeducation.com",
        "https://www.cbaeducation.com",
    ],
)

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

OPENEDX_BASE_URL = env("OPENEDX_BASE_URL", default="https://learn.cbaeducation.com")
OPENEDX_STUDIO_URL = env("OPENEDX_STUDIO_URL", default="https://studio.cbaeducation.com")
OPENEDX_CLIENT_ID = env("OPENEDX_CLIENT_ID", default="")
OPENEDX_CLIENT_SECRET = env("OPENEDX_CLIENT_SECRET", default="")
OPENEDX_API_TOKEN = env("OPENEDX_API_TOKEN", default="")

EMAIL_HOST = env("EMAIL_HOST", default="smtp.sendgrid.net")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="noreply@cbaeducation.com")

try:
    from .local import *
except ImportError:
    pass
