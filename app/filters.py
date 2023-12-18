from django_filters import rest_framework as filters

from .models import ModelJobPosting


class JobPostingFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = filters.CharFilter(field_name='country', lookup_expr='iexact')
    salary_min = filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = filters.NumberFilter(field_name='salary', lookup_expr='lte')

    class Meta:
        model = ModelJobPosting
        fields = [
            'name',
            'country'
        ]
