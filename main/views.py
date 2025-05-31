from django.views.generic import ListView, DetailView
from .models import CV


class CVListView(ListView):
    model = CV
    template_name = "main/index.html"
    context_object_name = "cvs"

    def get_queryset(self):
        queryset = CV.objects.prefetch_related("skills", "projects", "contacts")
        return queryset


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = self.object.skills.all()
        context["projects"] = self.object.projects.all()
        context["contacts"] = self.object.contacts.all()
        return context
