from django.views.generic import ListView
from .models import CV


class CVListView(ListView):
    model = CV
    template_name = "main/index.html"
    context_object_name = "cvs"

    def get_queryset(self):
        queryset = CV.objects.prefetch_related("skills", "projects", "contacts")
        return queryset
