from django.views import generic
from .models import Request


class SqlDebugList(generic.ListView):
    queryset = Request.objects.order_by('-load_date').values('id', 'path', 'total_sql_queries', 'total_time', 'load_date')
    context_object_name = 'requests'
    template_name = 'sql_debug/sql_debug_list.html'


class SqlDebugDetail(generic.DetailView):
    model = Request
    context_object_name = 'request_debug'
    template_name = 'sql_debug/sql_debug_detail.html'
