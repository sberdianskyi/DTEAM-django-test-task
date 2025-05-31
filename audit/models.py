from django.db import models
from django.contrib.auth.models import User


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_string = models.TextField(blank=True, null=True)
    remote_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    response_code = models.IntegerField()
    execution_time = models.FloatField(
        help_text="Request execution time in milliseconds"
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.timestamp} - {self.method} {self.path} ({self.response_code})"
