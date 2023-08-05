import json
import uuid
import sqlparse
from django.db import models
from . import settings


class Request(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    path = models.CharField(max_length=250)
    total_sql_queries = models.PositiveSmallIntegerField()
    queries = models.TextField()
    total_time = models.PositiveSmallIntegerField()
    load_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding and Request.objects.count() >= settings.MAX_REQUESTS:
            Request.objects.order_by('load_date').first().delete()
        super().save(*args, **kwargs)

    @property
    def json_queries(self):
        queries = json.loads(self.queries)
        for query in queries:
            query['sql'] = sqlparse.format(query['sql'], reindent=True, keyword_case='upper')
        return queries
