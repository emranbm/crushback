from backend.settings import *

# TODO: Make DEBUG false when the static files are served standalone.
DEBUG = True
ALLOWED_HOSTS = ['*']
DRF_RECAPTCHA_TESTING = False

CSRF_TRUSTED_ORIGINS = ['https://api.crushback.net']
