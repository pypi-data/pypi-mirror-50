from django.conf import settings

BLACKLISTED_PATHS = getattr(settings, 'SQL_DEBUG_BLACKLISTED_PATHS', [
    '/sql_debug',
    '/admin',
    '/favicon.ico',
])

MAX_REQUESTS = getattr(settings, 'SQL_DEBUG_MAX_REQUESTS', 15)
