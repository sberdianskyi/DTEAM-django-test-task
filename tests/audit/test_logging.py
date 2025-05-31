import time

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from audit.models import RequestLog


class LoggingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.cv_list_url = reverse("main:cv_list")

    def test_request_logging(self):
        # Test logging for anonymous user
        response = self.client.get(self.cv_list_url)
        self.assertEqual(response.status_code, 200)

        log = RequestLog.objects.latest("timestamp")
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, self.cv_list_url)
        self.assertIsNotNone(log.remote_ip)
        self.assertIsNone(log.user)
        self.assertEqual(log.response_code, 200)
        self.assertGreater(log.execution_time, 0)

    def test_authenticated_user_logging(self):
        # Test logging for authenticated user
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.cv_list_url)
        self.assertEqual(response.status_code, 200)

        log = RequestLog.objects.latest("timestamp")
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, self.cv_list_url)
        self.assertIsNotNone(log.remote_ip)
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.response_code, 200)
        self.assertGreater(log.execution_time, 0)

    def test_logs_limit(self):
        # Create 15 requests
        for _ in range(15):
            self.client.get(self.cv_list_url)
            time.sleep(0.1)

        # Check that only last 10 logs are shown on the page
        logs_url = reverse("audit:request_logs")
        response = self.client.get(logs_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["logs"]), 10)

        # Verify ordering (newest to oldest)
        logs = response.context["logs"]
        for i in range(len(logs) - 1):
            self.assertGreater(logs[i].timestamp, logs[i + 1].timestamp)
