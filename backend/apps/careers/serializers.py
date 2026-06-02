from rest_framework import serializers
from .models import SavedCareerRecommendation


class CareerPredictionSerializer(serializers.Serializer):

    interests = serializers.ListField(
        child=serializers.CharField()
    )

    skills = serializers.ListField(
        child=serializers.CharField()
    )

    personality = serializers.ListField(
        child=serializers.CharField()
    )

    goals = serializers.ListField(
        child=serializers.CharField()
    )

class SavedCareerRecommendationSerializer(serializers.ModelSerializer):

    class Meta:

        model = SavedCareerRecommendation

        fields = '__all__'

        read_only_fields = ['user']