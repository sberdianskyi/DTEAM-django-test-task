from django.views.generic import ListView
from .models import RequestLog


class RequestLogListView(ListView):
    model = RequestLog
    template_name = "audit/request_logs.html"
    context_object_name = "logs"

    def get_queryset(self):
        queryset = RequestLog.objects.select_related("user")[:10]
        return queryset
