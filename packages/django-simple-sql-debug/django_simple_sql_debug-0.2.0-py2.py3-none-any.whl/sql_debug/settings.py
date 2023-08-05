from django.conf import settings

PATHS_BLACKLIST = getattr(settings, 'SQL_DEBUG_PATHS_BLACKLIST', [
    '/sql_debug',
    '/admin',
    '/favicon.ico',
])

MAX_REQUESTS = getattr(settings, 'SQL_DEBUG_MAX_REQUESTS', 20)
