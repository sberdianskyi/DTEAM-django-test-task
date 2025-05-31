from django.urls import path
from .views import CVListView

app_name = "main"

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
]
