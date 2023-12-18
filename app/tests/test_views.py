from unittest import mock
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import ModelJobAlert, ModelJobPosting, ModelSkill


def mock_get(status_code=200):
    class MockResponse:
        def __init__(self):
            self.status_code = status_code

        @staticmethod
        def json():
            return [
                ["Developer", 30000, "Argentina", ["OOP", "PHP", "MySQL"]],
                ["DBA", 35000, "Spain", ["MySQL", "Percona", "Bash"]],
            ]

    return MockResponse()


class ModelSKillViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_model_skill_response_status(self):
        """
        Add a skill and return a status code 201
        Call the skill api and return a status code 200
        """
        data_json = {"skill": "Java"}

        url = reverse("skill-list")
        response = self.client.post(url, data=data_json, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["skill"], "Java")


class ModelJobAlertsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_model_job_alert_response_status(self):
        """
        Add a job alert and return a status code 201
        Call the job_alert api and return a status code 200
        """
        data_json = {
            "email": "fedemarkco@gmail.com",
            "name": "Java",
            "country": "Argentina",
            "salary_min": 30000,
            "salary_max": 35000,
        }

        url = reverse("job_alert-list")
        response = self.client.post(url, data=data_json, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_json["email"], response.json()[0]["email"])


class ModelJobPostingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("app.notifications.send_mail")
    @override_settings(SENDER="fedemarkco@gmail.com")
    def test_model_job_posting_with_notification_filter(self, mock_send_mail):
        """
        Add a job_alert (with filters) and
        a job posting, return a status code 201
        Call the job_posting api and return a
        status code 200
        """
        ModelSkill.objects.create(skill="Java")
        ModelSkill.objects.create(skill="OOP")

        job_posting_json = {
            "name": "SSr Java Developer",
            "salary": 32000,
            "country": "Argentina",
            "skill": [1, 2],
        }

        job_alert_json = {
            "email": "fedemarkco@gmail.com",
            "name": "Java",
            "country": "Argentina",
            "salary_min": 30000,
            "salary_max": 35000,
        }

        job_alert_url = reverse("job_alert-list")
        job_alert_response = self.client.post(
            job_alert_url, data=job_alert_json, format="json"
        )

        self.assertEqual(
            job_alert_response.status_code, status.HTTP_201_CREATED)

        job_alert = ModelJobAlert.objects.first()

        self.assertEqual(str(job_alert), "fedemarkco@gmail.com")

        job_posting_url = reverse("job_posting-list")
        job_posting_response = self.client.post(
            job_posting_url, data=job_posting_json, format="json"
        )

        self.assertEqual(
            job_posting_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(job_posting_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["name"], "SSr Java Developer")

        job_posting = ModelJobPosting.objects.first()

        self.assertEqual(str(job_posting), "SSr Java Developer")

        self.assertTrue(mock_send_mail.called)

    @patch("app.notifications.send_mail")
    @override_settings(SENDER="fedemarkco@gmail.com")
    @override_settings(SOURCE_EXTERN="https://service_extern/jobs")
    @mock.patch("requests.get", side_effect=[mock_get(status_code=200)])
    def test_model_job_posting_without_notification_filter(
        self, mock_send_mail, mock_requests_get
    ):
        """
        Add two skills, a job alert (without filters)
        and a job posting, return a status code 201
        Call the job_posting api and return a status code 200
        """
        ModelSkill.objects.create(skill="Java")
        ModelSkill.objects.create(skill="OOP")

        job_posting_json = {
            "name": "SSr Java Developer",
            "salary": 32000,
            "country": "Argentina",
            "skill": [1, 2],
        }

        job_alert_json = {"email": "fedemarkco@gmail.com"}

        job_alert_url = reverse("job_alert-list")
        job_alert_response = self.client.post(
            job_alert_url, data=job_alert_json, format="json"
        )

        self.assertEqual(
            job_alert_response.status_code, status.HTTP_201_CREATED)

        job_alert = ModelJobAlert.objects.first()

        self.assertEqual(str(job_alert), "fedemarkco@gmail.com")

        job_posting_url = reverse("job_posting-list")
        job_posting_response = self.client.post(
            job_posting_url, data=job_posting_json, format="json"
        )

        self.assertEqual(
            job_posting_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(job_posting_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["name"], "SSr Java Developer")

        job_posting = ModelJobPosting.objects.first()

        self.assertEqual(str(job_posting), "SSr Java Developer")

        self.assertTrue(mock_send_mail.called)
