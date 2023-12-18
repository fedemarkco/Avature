from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from .filters import JobPostingFilter
from .models import ModelJobAlert, ModelJobPosting, ModelSkill
from .notifications import notification_job_alert
from .serializers import (
    ModelCreateJobPostingSerializer,
    ModelJobAlertSerializer,
    ModelSearchJobPostingSerializer,
    ModelSkillSerializer,
)
from .services import JobberwockyExteneralJobs


class ModelSKillViewSet(viewsets.ModelViewSet):
    """
    This view gets a list of skills
    Return:
    [
        {
            "id": integer,
            "skill": string
        }
    ]

    It also allows you to add skills
    Json of post method:
    {
        "skill": string
    }

    """

    queryset = ModelSkill.objects.all()
    serializer_class = ModelSkillSerializer
    http_method_names = ["get", "post"]


class ModelJobPostingViewSet(viewsets.ModelViewSet):
    """
    This view gets a list of job posting
    Get internal and external job posting
    Return:
    [
        {
            "name": string,
            "salary": integer,
            "country": string,
            "skill": [
                string
            ]
        }
    ]

    It also allows you to add job posting
    skill, it would be a list of id
    Json of post method:
    {
        "name": string,
        "salary": integer,
        "country": string,
        "skill": [
            integer
        ]
    }

    """

    queryset = ModelJobPosting.objects.all()
    serializer_class = ModelSearchJobPostingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobPostingFilter
    http_method_names = ["get", "post"]

    def list(self, request):
        source_extern = self.add_source_extern(
            request.query_params.urlencode())
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data + source_extern)

    def add_source_extern(self, params):
        source_extern = JobberwockyExteneralJobs(params)
        response_extern = []
        if source_extern["Status"] == "Ok":
            for source in source_extern["Response"]:
                data = {
                    "name": source[0],
                    "salary": source[1],
                    "country": source[2],
                    "skill": source[3],
                }
                response_extern.append(data)

        return response_extern

    def create(self, request):
        data = request.data
        serializer = ModelCreateJobPostingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        notification_job_alert(data)
        return Response(status=status.HTTP_201_CREATED)


class ModelJobAlertsViewSet(viewsets.ModelViewSet):
    """
    This view gets a list of job alerts
    Return:
    [
        {
            "id": integer,
            "email": string,
            "created_date": datetime,
            "name": string,
            "country": string,
            "salary_min": integer,
            "salary_max": integer
        }
    ]

    It also allows you to add job alert
    Json of post method:
    {
        "email": string,
        "name": string (optional),
        "country": string (optional),
        "salary_min": integer (optional),
        "salary_max": integer (optional)
    }

    """

    queryset = ModelJobAlert.objects.all()
    serializer_class = ModelJobAlertSerializer
    http_method_names = ["get", "post"]

    def create(self, request):
        data = request.data
        serializer = ModelJobAlertSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
