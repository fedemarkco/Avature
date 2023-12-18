from django.urls import include, path
from rest_framework import routers

from .views import (ModelJobAlertsViewSet, ModelJobPostingViewSet,
                    ModelSKillViewSet)

router = routers.DefaultRouter()
router.register(r'skill', ModelSKillViewSet, basename='skill')
router.register(r'job-posting', ModelJobPostingViewSet, basename='job_posting')
router.register(r'job-alert', ModelJobAlertsViewSet, basename='job_alert')

urlpatterns = [
    path('', include(router.urls))
]
