from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

from .models import UserProfile, IkigaiResponse, IkigaiScore
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    IkigaiResponseSerializer,
    IkigaiScoreSerializer,
)

User = get_user_model()


def calculate_ikigai_scores(response_data):
    mapping = {
        'frontend': 0,
        'backend': 0,
        'fullstack': 0,
        'data_science': 0,
        'ai_ml': 0,
    }

    def add(path, amount=1):
        mapping[path] += amount

    passion = [item.lower() for item in response_data.get('passion', [])]
    skills = [item.lower() for item in response_data.get('skills', [])]
    impact = [item.lower() for item in response_data.get('impact', [])]
    career = [item.lower() for item in response_data.get('career', [])]

    for item in passion:
        if 'designing ui' in item or 'building apps' in item:
            add('frontend', 2)
            add('fullstack', 1)
        if 'coding problems' in item:
            add('backend', 1)
            add('fullstack', 1)
        if 'data analysis' in item:
            add('data_science', 2)
            add('ai_ml', 1)
        if 'system design' in item:
            add('backend', 2)
            add('fullstack', 1)

    for item in skills:
        if any(term in item for term in ['html', 'css', 'javascript', 'react']):
            add('frontend', 2)
            add('fullstack', 1)
        if any(term in item for term in ['python', 'sql']):
            add('backend', 1)
            add('data_science', 1)
            add('ai_ml', 1)
            add('fullstack', 1)

    for item in impact:
        if 'ux' in item:
            add('frontend', 2)
        if 'systems' in item:
            add('backend', 2)
            add('fullstack', 1)
        if 'ai' in item or 'data' in item:
            add('data_science', 2)
            add('ai_ml', 2)
        if 'real-world' in item:
            add('fullstack', 2)
            add('backend', 1)

    for item in career:
        if 'frontend' in item:
            add('frontend', 3)
        if 'backend' in item:
            add('backend', 3)
        if 'full stack' in item or 'fullstack' in item:
            add('fullstack', 3)
        if 'data science' in item:
            add('data_science', 3)
        if 'ai' in item or 'ml' in item:
            add('ai_ml', 3)

    best_fit = max(mapping, key=mapping.get)
    career_labels = {
        'frontend': 'Frontend Development',
        'backend': 'Backend Development',
        'fullstack': 'Full Stack Development',
        'data_science': 'Data Science',
        'ai_ml': 'AI/ML',
    }
    result_text = f"You are highly aligned with {career_labels[best_fit]} based on your interests, skills, and goals."

    return mapping, career_labels[best_fit], result_text


class SignupView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User created successfully',
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile_complete = profile.is_profile_complete
            return Response({
                'message': 'Login successful',
                'email': user.email,
                'full_name': user.full_name,
                'token': token.key,
                'profile_complete': profile_complete,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_profile(self, user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self.get_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_profile(request.user)

        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            updated_profile = serializer.save()

            updated_profile.is_profile_complete = True
            updated_profile.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        profile = self.get_profile(request.user)

        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():

            updated_profile = serializer.save()

            updated_profile.is_profile_complete = True
            updated_profile.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class IkigaiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = UserProfile.objects.get_or_create(user=request.user)[0]
        serializer = IkigaiResponseSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.validated_data
            IkigaiResponse.objects.update_or_create(profile=profile, defaults=response_data)
            mapping, best_fit, result_text = calculate_ikigai_scores(response_data)
            score_data = {
                'frontend_score': mapping['frontend'],
                'backend_score': mapping['backend'],
                'fullstack_score': mapping['fullstack'],
                'data_science_score': mapping['data_science'],
                'ai_ml_score': mapping['ai_ml'],
                'best_fit': best_fit.title() if best_fit != 'ai_ml' else 'AI/ML',
                'result_text': result_text,
            }
            IkigaiScore.objects.update_or_create(profile=profile, defaults=score_data)
            score = IkigaiScore.objects.get(profile=profile)
            score_serializer = IkigaiScoreSerializer(score)
            return Response(score_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IkigaiResultView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        try:
            score = profile.ikigai_score
            serializer = IkigaiScoreSerializer(score)
            return Response(serializer.data)
        except IkigaiScore.DoesNotExist:
            return Response({'detail': 'No Ikigai result found.'}, status=status.HTTP_404_NOT_FOUND)
