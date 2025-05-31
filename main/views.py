from django.views import generic
from django_weasyprint import WeasyTemplateResponseMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import CV
from .serializers import CVSerializer


class CVContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skills"] = self.object.skills.all()
        context["projects"] = self.object.projects.all()
        context["contacts"] = self.object.contacts.all()
        return context


class CVListView(generic.ListView):
    model = CV
    template_name = "main/index.html"
    context_object_name = "cvs"
    paginate_by = 5

    def get_queryset(self):
        queryset = CV.objects.prefetch_related("skills", "projects", "contacts")
        return queryset


class CVDetailView(CVContextMixin, generic.DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"


class CVPDFView(WeasyTemplateResponseMixin, CVContextMixin, generic.DetailView):
    model = CV
    template_name = "main/cv_pdf.html"
    context_object_name = "cv"
    pdf_filename = "cv.pdf"


@extend_schema(tags=["CVs"])
class CVViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CV records.
    Supports CRUD operations for CVs including nested skills, projects and contacts.
    """

    queryset = CV.objects.prefetch_related("skills", "projects", "contacts").order_by(
        "id"
    )
    serializer_class = CVSerializer

    @extend_schema(
        summary="List CVs",
        description="Returns a list of all CVs with their related data",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create CV",
        description="Creates a new CV with nested skills, projects and contacts",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve CV", description="Returns details of a specific CV"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update CV", description="Updates an existing CV (full update)"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update CV",
        description="Updates an existing CV (partial update)",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="Delete CV", description="Deletes a CV")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
