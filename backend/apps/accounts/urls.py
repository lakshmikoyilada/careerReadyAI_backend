from django.urls import path
from .views import SignupView, LoginView, UserListView, ProfileView, IkigaiView, IkigaiResultView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('ikigai/', IkigaiView.as_view(), name='ikigai-submit'),
    path('ikigai/result/', IkigaiResultView.as_view(), name='ikigai-result'),
]
