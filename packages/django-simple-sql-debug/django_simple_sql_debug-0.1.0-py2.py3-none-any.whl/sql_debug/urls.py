from django.urls import path
from .views import SqlDebugList, SqlDebugDetail

app_name = 'sql_debug'

urlpatterns = [
    path('', SqlDebugList.as_view(), name='list'),
    path('<uuid:pk>/', SqlDebugDetail.as_view(), name='detail'),
]
