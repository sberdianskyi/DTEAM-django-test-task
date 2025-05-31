from django.views.generic import ListView, DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from .models import CV


class CVContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = self.object.skills.all()
        context["projects"] = self.object.projects.all()
        context["contacts"] = self.object.contacts.all()
        return context


class CVListView(ListView):
    model = CV
    template_name = "main/index.html"
    context_object_name = "cvs"

    def get_queryset(self):
        queryset = CV.objects.prefetch_related("skills", "projects", "contacts")
        return queryset


class CVDetailView(CVContextMixin, DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"


class CVPDFView(WeasyTemplateResponseMixin, CVContextMixin, DetailView):
    model = CV
    template_name = "main/cv_pdf.html"
    context_object_name = "cv"
    pdf_filename = "cv.pdf"
