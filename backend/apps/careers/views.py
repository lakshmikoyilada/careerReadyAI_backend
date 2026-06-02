from .models import CareerRecommendation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SavedCareerRecommendation
from .serializers import SavedCareerRecommendationSerializer
from .serializers import CareerPredictionSerializer
from ai_engine.inference.recommend import recommend_careers
import pandas as pd
import os


class CareerPredictionView(APIView):

    def post(self, request):

        serializer = CareerPredictionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            data = serializer.validated_data

            user_profile_text = " ".join(

                data["interests"] +
                data["skills"] +
                data["personality"] +
                data["goals"]

            )

            prediction = recommend_careers(
                user_profile_text
            )

            CareerRecommendation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                recommended_career=str(prediction)
            )

            return Response(
                {
                    "success": True,
                    "recommended_careers": prediction
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class SaveCareerRecommendationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        recommendations = request.data.get('recommendations', [])

        saved_items = []

        for recommendation in recommendations:

            saved_recommendation = SavedCareerRecommendation.objects.create(

    user=request.user,

    career_name=recommendation['career'],

    score=recommendation['score']

)

            saved_items.append(saved_recommendation)

        serializer = SavedCareerRecommendationSerializer(
                saved_items,
                many=True
            )

        return Response({

            'success': True,
            'saved_recommendations': serializer.data

        })
    
class UserRecommendationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        recommendations = SavedCareerRecommendation.objects.filter(
                user=request.user
            ).order_by('-created_at')

        serializer = SavedCareerRecommendationSerializer(
                recommendations,
                many=True
            )

        return Response({

            'success': True,
            'recommendations': serializer.data

        })
    
class CareerDetailsView(APIView):

    def get(self, request, career_name):

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        dataset_path = os.path.join(
            BASE_DIR,
            "ai_engine",
            "datasets",
            "career_master_dataset.csv"
        )

        df = pd.read_csv(dataset_path)

        career = df[
            df["career"] == career_name
        ]

        if career.empty:

            return Response(
                {
                    "success": False,
                    "message": "Career not found"
                },
                status=404
            )

        row = career.iloc[0]

        return Response({

            "success": True,

            "career": {
                "career": row["career"],
                "description": row["description"],
                "career_category": row["career_category"],
                "salary_range": row["salary_range"],
                "future_scope": row["future_scope"],
                "technical_skills": row["technical_skills"],
                "certifications": row["certifications"],
                "projects": row["projects"],
                "roadmap": row["roadmap"]
            }

        })