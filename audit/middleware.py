import time
from typing import Any
from django.http import HttpRequest, HttpResponse

from .models import RequestLog


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Start timing the request
        start_time = time.time()

        # Get the response
        response = self.get_response(request)

        # Calculate execution time in milliseconds
        execution_time = (time.time() - start_time) * 1000

        # Create the log entry
        RequestLog.objects.create(
            method=request.method,
            path=request.path,
            query_string=request.META.get("QUERY_STRING", ""),
            remote_ip=self.get_client_ip(request),
            user=request.user if request.user.is_authenticated else None,
            response_code=response.status_code,
            execution_time=execution_time,
        )

        return response

    def get_client_ip(self, request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
