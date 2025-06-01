from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CVListView,
    CVDetailView,
    CVPDFView,
    CVViewSet,
    SettingsView,
    SendCVPDFView,
    TranslateCVView,
)

app_name = "main"

router = DefaultRouter()
router.register("api/cvs", CVViewSet)

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", CVPDFView.as_view(), name="cv_pdf"),
    path("cv/<int:pk>/send_pdf/", SendCVPDFView.as_view(), name="cv_send_pdf"),
    path("cv/<int:pk>/translate/", TranslateCVView.as_view(), name="cv_translate"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("", include(router.urls)),
]
