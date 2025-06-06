import base64

from django.views import generic
from django.http import JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django_weasyprint import WeasyTemplateResponseMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import CV
from .serializers import CVSerializer
from .tasks import send_cv_pdf_task
from .translation import translate_text


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


class SendCVPDFView(CVPDFView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "Only POST method is allowed"}, status=405)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"message": "Email required."}, status=400)

        try:
            self.object = self.get_object()
            filename = f"CV_{self.object.first_name}_{self.object.last_name}"

            # Generating PDF
            context = self.get_context_data()
            html_string = render_to_string(self.template_name, context)
            pdf_content = HTML(string=html_string).write_pdf()

            # Convert PDF to base64
            pdf_content_base64 = base64.b64encode(pdf_content).decode("utf-8")

            task = send_cv_pdf_task.apply_async(
                args=[email, pdf_content_base64, filename],
            )

            result = task.get(timeout=30)
            return JsonResponse(
                {"message": "PDF sent to email!" if result else "Failed to send email"},
                status=200 if result else 500,
            )

        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)


class TranslateCVView(CVContextMixin, generic.DetailView):
    model = CV
    template_name = "main/cv_detail.html"

    def post(self, request, *args, **kwargs):
        language = request.POST.get("language")
        if not language:
            return JsonResponse({"error": "Language is required"}, status=400)

        self.object = self.get_object()

        # Collecting the main text of the CV
        text_to_translate = f"""
    First Name: {self.object.first_name}
    Last Name: {self.object.last_name}
    Bio: {self.object.bio}
    Projects:
    """

        # Adding information about projects
        for project in self.object.projects.all():
            text_to_translate += f"""
    Project: {project.name}
    Description: {project.description}
    """

        translated_text = translate_text(text_to_translate, language)
        return JsonResponse({"translated_text": translated_text})


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


class SettingsView(generic.TemplateView):
    template_name = "main/settings.html"
