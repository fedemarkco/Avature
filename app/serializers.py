from rest_framework import serializers

from .models import ModelJobAlert, ModelJobPosting, ModelSkill


class ModelSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSkill
        fields = '__all__'


class ModelSearchJobPostingSerializer(serializers.ModelSerializer):
    skill = serializers.StringRelatedField(many=True)

    class Meta:
        model = ModelJobPosting
        fields = [
            'name',
            'salary',
            'country',
            'skill'
        ]


class ModelCreateJobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelJobPosting
        fields = [
            'name',
            'salary',
            'country',
            'skill'
        ]


class ModelJobAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelJobAlert
        fields = "__all__"
