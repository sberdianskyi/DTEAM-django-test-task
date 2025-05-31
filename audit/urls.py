from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("logs/", views.RequestLogListView.as_view(), name="request_logs"),
]
