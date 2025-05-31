from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from main.models import CV, Skill, Project, Contact
from datetime import date

CV_LIST_URL = reverse("main:cv_list")


class CVViewsTest(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()

        # Create test CV
        self.cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Test biography"
        )

        # Create related objects
        self.skill = Skill.objects.create(cv=self.cv, name="Python", level="Advanced")

        self.project = Project.objects.create(
            cv=self.cv,
            name="Test Project",
            description="Test description",
            technologies="Python, Django",
            start_date=date(2024, 1, 1),
        )

        self.contact = Contact.objects.create(
            cv=self.cv, type="Email", value="john@example.com"
        )

    def test_cv_list_view(self):
        # Test CV list page
        res = self.client.get(CV_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/index.html")
        self.assertContains(res, "John Doe")
        self.assertContains(res, "Test biography")
        self.assertContains(res, "Python")

    def test_cv_detail_view(self):
        # Test CV detail page
        res = self.client.get(reverse("main:cv_detail", kwargs={"pk": self.cv.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main/cv_detail.html")
        self.assertContains(res, "John Doe")
        self.assertContains(res, "Test biography")
        self.assertContains(res, "Python")
        self.assertContains(res, "Test Project")
        self.assertContains(res, "john@example.com")

    def test_cv_detail_view_404(self):
        # Test non-existent CV
        res = self.client.get(reverse("main:cv_detail", kwargs={"pk": 500}))
        self.assertEqual(res.status_code, 404)
