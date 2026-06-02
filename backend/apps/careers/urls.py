from django.urls import path

from .views import CareerPredictionView
from .views import SaveCareerRecommendationView
from .views import UserRecommendationsView
from .views import CareerDetailsView


urlpatterns = [
    path(
        'predict/',
        CareerPredictionView.as_view(),
        name='career-predict'
    ),
    path(
    'save-recommendations/',
    SaveCareerRecommendationView.as_view()
),
path(
    'user-recommendations/',
    UserRecommendationsView.as_view()
),
path(
    "details/<str:career_name>/",
    CareerDetailsView.as_view()
),
]