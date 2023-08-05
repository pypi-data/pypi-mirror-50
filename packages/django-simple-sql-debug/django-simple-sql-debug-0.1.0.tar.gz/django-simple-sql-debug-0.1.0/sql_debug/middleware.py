import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from . import settings
from .models import Request


class SqlDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not self.is_blacklisted(request.path):
            queries = connection.queries
            Request.objects.create(
                path=request.path,
                total_sql_queries=len(queries),
                queries=json.dumps(queries, cls=DjangoJSONEncoder),
                total_time=sum(float(query['time']) for query in queries) if queries else 0,
            )
        return response

    @staticmethod
    def is_blacklisted(request_path):
        for path in settings.BLACKLISTED_PATHS:
            if request_path.startswith(path):
                return True
        return False
