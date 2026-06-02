from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import (
    UserProfile,
    Skill,
    UserSkill,
    Goal,
    LearningPreference,
    UserInterest,
    UserChallenge,
    IkigaiResponse,
    IkigaiScore,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'created_at')
        read_only_fields = ('id', 'created_at')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()

    class Meta:
        model = UserSkill
        fields = ('id', 'skill', 'level', 'rating')

    def create(self, validated_data):
        skill_data = validated_data.pop('skill')
        skill, _ = Skill.objects.get_or_create(name=skill_data['name'])
        return UserSkill.objects.create(skill=skill, **validated_data)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('career_goal', 'timeline', 'purpose')


class LearningPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPreference
        fields = ('hours_per_day', 'learning_style')


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ('id', 'interest_area', 'preferred_method', 'confidence_level')


class UserChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChallenge
        fields = ('id', 'challenge')


class IkigaiResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IkigaiResponse
        fields = ('passion', 'skills', 'impact', 'career')


class IkigaiScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = IkigaiScore
        fields = ('frontend_score', 'backend_score', 'fullstack_score', 'data_science_score', 'ai_ml_score', 'best_fit', 'result_text')


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_skills = UserSkillSerializer(many=True, required=False)
    goal = GoalSerializer(required=False)
    learning_preferences = LearningPreferenceSerializer(required=False)
    interests = UserInterestSerializer(many=True, required=False)
    challenges = UserChallengeSerializer(many=True, required=False)
    ikigai_response = IkigaiResponseSerializer(required=False)
    ikigai_score = IkigaiScoreSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
    'email',
    'full_name',
    'is_profile_complete',

    'phone_number',
    'role',
    'education',
    'branch',
    'year',
    'previous_projects',
    'github_link',
    'portfolio_link',
    'bio',
    'career_goal',
    'timeline',
    'purpose',
    'hours_per_day',
    'learning_style',
    'confidence_level',
    'user_skills',
    'goal',
    'learning_preferences',
    'interests',
    'challenges',
    'ikigai_response',
    'ikigai_score',
)

    def update(self, instance, validated_data):
        user_skills_data = validated_data.pop('user_skills', None)
        goal_data = validated_data.pop('goal', None)
        learning_preferences_data = validated_data.pop('learning_preferences', None)
        interests_data = validated_data.pop('interests', None)
        challenges_data = validated_data.pop('challenges', None)
        ikigai_response_data = validated_data.pop('ikigai_response', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if goal_data is not None:
            Goal.objects.update_or_create(profile=instance, defaults=goal_data)

        if learning_preferences_data is not None:
            LearningPreference.objects.update_or_create(profile=instance, defaults=learning_preferences_data)

        if user_skills_data is not None:
            instance.user_skills.all().delete()
            for skill_item in user_skills_data:
                skill_data = skill_item.pop('skill')
                skill, _ = Skill.objects.get_or_create(name=skill_data['name'])
                UserSkill.objects.create(profile=instance, skill=skill, **skill_item)

        if interests_data is not None:
            instance.interests.all().delete()
            for interest_item in interests_data:
                UserInterest.objects.create(profile=instance, **interest_item)

        if challenges_data is not None:
            instance.challenges.all().delete()
            for challenge_item in challenges_data:
                UserChallenge.objects.create(profile=instance, **challenge_item)

        if ikigai_response_data is not None:
            IkigaiResponse.objects.update_or_create(profile=instance, defaults=ikigai_response_data)

        return instance

    def create(self, validated_data):
        user_skills_data = validated_data.pop('user_skills', None)
        goal_data = validated_data.pop('goal', None)
        learning_preferences_data = validated_data.pop('learning_preferences', None)
        interests_data = validated_data.pop('interests', None)
        challenges_data = validated_data.pop('challenges', None)
        ikigai_response_data = validated_data.pop('ikigai_response', None)

        user = self.context['request'].user
        instance = UserProfile.objects.create(user=user, **validated_data)

        if goal_data is not None:
            Goal.objects.create(profile=instance, **goal_data)

        if learning_preferences_data is not None:
            LearningPreference.objects.create(profile=instance, **learning_preferences_data)

        if user_skills_data is not None:
            for skill_item in user_skills_data:
                skill_data = skill_item.pop('skill')
                skill, _ = Skill.objects.get_or_create(name=skill_data['name'])
                UserSkill.objects.create(profile=instance, skill=skill, **skill_item)

        if interests_data is not None:
            for interest_item in interests_data:
                UserInterest.objects.create(profile=instance, **interest_item)

        if challenges_data is not None:
            for challenge_item in challenges_data:
                UserChallenge.objects.create(profile=instance, **challenge_item)

        if ikigai_response_data is not None:
            IkigaiResponse.objects.create(profile=instance, **ikigai_response_data)

        return instance

    def validate(self, data):
        role = data.get('role')
        if role and role not in ['Student', 'Professional']:
            raise serializers.ValidationError({'role': 'Role must be Student or Professional'})
        return data


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password_confirm']

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match"})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data
