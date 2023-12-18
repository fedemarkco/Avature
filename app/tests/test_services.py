from unittest import mock

from django.test import TestCase, override_settings

from ..services import JobberwockyExteneralJobs


def mock_get(status_code=200):
    class MockResponse:
        def __init__(self):
            self.status_code = status_code

        @staticmethod
        def json():
            return [
                ['Developer', 30000, 'Argentina', ['OOP', 'PHP', 'MySQL']],
                ['DBA', 35000, 'Spain', ['MySQL', 'Percona', 'Bash']]
            ]

    return MockResponse()


class ServiceExternTestCase(TestCase):
    """
    Different tests to test the external service, Status tests,
    the possible values can be Ok or Error
​
    """
    @override_settings(SOURCE_EXTERN='')
    def test_service_extern_without_source_extern(self):
        response = JobberwockyExteneralJobs()
        self.assertEqual(response['Status'], 'Error')

    @override_settings(SOURCE_EXTERN='https://service_extern/jobs')
    def test_service_extern_with_params_and_status_error(self):
        response = JobberwockyExteneralJobs('name=Java')
        self.assertEqual(response['Status'], 'Error')

    @override_settings(SOURCE_EXTERN='https://service_extern/jobs')
    @mock.patch('requests.get', side_effect=[mock_get(status_code=200)])
    def test_service_extern_status_code_200(self, mock_requests_get):
        response = JobberwockyExteneralJobs()
        self.assertEqual(response['Status'], 'Ok')

    @override_settings(SOURCE_EXTERN='https://service_extern/jobs')
    @mock.patch('requests.get', side_effect=[mock_get(status_code=500)])
    def test_service_extern_status_code_500(self, mock_requests_get):
        response = JobberwockyExteneralJobs()
        self.assertEqual(response['Status'], 'Error')
