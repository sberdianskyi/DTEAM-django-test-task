from django.urls import path
from .views import CVListView, CVDetailView, CVPDFView

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", CVPDFView.as_view(), name="cv_pdf"),
]
