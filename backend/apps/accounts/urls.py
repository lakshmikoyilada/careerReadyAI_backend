from django.urls import path
from .views import SignupView, LoginView, UserListView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),
]
