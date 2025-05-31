from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import CV


class CVTests(APITestCase):
    def setUp(self):
        self.cv_data = {
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Python Developer",
            "skills": [
                {"name": "Python", "level": "Expert"},
                {"name": "Django", "level": "Advanced"},
            ],
            "projects": [
                {
                    "name": "Test Project",
                    "description": "A test project",
                    "technologies": "Python, Django",
                    "start_date": "2024-01-01",
                    "end_date": "2024-02-01",
                }
            ],
            "contacts": [{"type": "Email", "value": "john@example.com"}],
        }

    def test_create_cv(self):
        """Test creating a new CV"""
        url = reverse("main:cv-list")
        response = self.client.post(url, self.cv_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 1)
        self.assertEqual(CV.objects.get().first_name, "John")

    def test_get_cv_list(self):
        """Test retrieving CV list"""
        url = reverse("main:cv-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_cv_detail(self):
        """Test retrieving CV detail"""
        cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Python Developer"
        )
        url = reverse("main:cv-detail", args=(cv.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cv(self):
        """Test updating CV"""
        cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Python Developer"
        )
        url = reverse("main:cv-detail", args=(cv.id,))
        data = {"first_name": "Jane", "last_name": "Doe", "bio": "Python Developer"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CV.objects.get().first_name, "Jane")

    def test_delete_cv(self):
        """Test deleting CV"""
        cv = CV.objects.create(
            first_name="John", last_name="Doe", bio="Python Developer"
        )
        url = reverse("main:cv-detail", args=(cv.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)
