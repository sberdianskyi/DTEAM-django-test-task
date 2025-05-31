from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CVListView, CVDetailView, CVPDFView, CVViewSet

app_name = "main"

router = DefaultRouter()
router.register("api/cvs", CVViewSet)

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", CVPDFView.as_view(), name="cv_pdf"),
    path("", include(router.urls)),
]
