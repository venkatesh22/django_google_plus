from django.conf import settings

STORE_CREDENTIALS = getattr(
    settings, 'STORE_CREDENTIALS', True)

STORE_GMAIL_USER_CREDENTIALS = getattr(
    settings, 'STORE_GMAIL_USER_CREDENTIALS', True)

STORE_GOOGLE_APPS_USER_CREDENTIALS = getattr(
    settings, 'STORE_GOOGLE_APPS_USER_CREDENTIALS', True)

GOOGLE_CLIENT_ID = getattr(
    settings, 'GOOGLE_CLIENT_ID', None)

GOOGLE_CLIENT_SECRET = getattr(
    settings, 'GOOGLE_CLIENT_SECRET', None)
