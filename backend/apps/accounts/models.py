from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password):

        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Professional', 'Professional'),
    ]

    CAREER_GOAL_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Full Stack', 'Full Stack'),
        ('Data Science', 'Data Science'),
        ('AI/ML', 'AI/ML'),
    ]

    TIMELINE_CHOICES = [
        ('3 months', '3 months'),
        ('6 months', '6 months'),
        ('1 year', '1 year'),
    ]

    PURPOSE_CHOICES = [
        ('Job', 'Job'),
        ('Internship', 'Internship'),
        ('Freelancing', 'Freelancing'),
        ('Startup', 'Startup'),
    ]

    HOURS_CHOICES = [
        ('<1', '<1'),
        ('1–2', '1–2'),
        ('3–5', '3–5'),
        ('5+', '5+'),
    ]

    LEARNING_STYLE_CHOICES = [
        ('Video', 'Video'),
        ('Reading', 'Reading'),
        ('Practice', 'Practice'),
        ('Mixed', 'Mixed'),
    ]

    CONFIDENCE_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    is_profile_complete = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    education = models.CharField(max_length=255, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    previous_projects = models.TextField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    career_goal = models.CharField(max_length=255, blank=True, null=True)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True, null=True)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, blank=True, null=True)

    hours_per_day = models.CharField(max_length=10, choices=HOURS_CHOICES, blank=True, null=True)
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CHOICES, blank=True, null=True)
    confidence_level = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('profile', 'skill')

    def __str__(self):
        return f"{self.skill.name} ({self.level})"


class Goal(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='goal')
    career_goal = models.CharField(max_length=50, choices=UserProfile.CAREER_GOAL_CHOICES, blank=True, null=True)
    timeline = models.CharField(max_length=20, choices=UserProfile.TIMELINE_CHOICES, blank=True, null=True)
    purpose = models.CharField(max_length=20, choices=UserProfile.PURPOSE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Goal for {self.profile.user.email}"


class LearningPreference(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='learning_preferences')
    hours_per_day = models.CharField(max_length=10, choices=UserProfile.HOURS_CHOICES, blank=True, null=True)
    learning_style = models.CharField(max_length=20, choices=UserProfile.LEARNING_STYLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Learning pref for {self.profile.user.email}"


class UserInterest(models.Model):
    INTEREST_CHOICES = [
    ('Technology', 'Technology'),
    ('Artificial Intelligence', 'Artificial Intelligence'),
    ('Data Science', 'Data Science'),
    ('Cybersecurity', 'Cybersecurity'),
    ('UI/UX Design', 'UI/UX Design'),
    ('Business', 'Business'),
    ('Marketing', 'Marketing'),
    ('Finance', 'Finance'),
    ('Healthcare', 'Healthcare'),
    ('Teaching', 'Teaching'),
    ('Law', 'Law'),
    ('Content Creation', 'Content Creation'),
    ('Entrepreneurship', 'Entrepreneurship'),
    ('Research', 'Research'),
]

    METHOD_CHOICES = [
        ('Projects', 'Projects'),
        ('Tutorials', 'Tutorials'),
        ('Coding Problems', 'Coding Problems'),
        ('Reading', 'Reading'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='interests')
    interest_area = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    preferred_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    confidence_level = models.CharField(max_length=10, choices=UserProfile.CONFIDENCE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.interest_area} interest for {self.profile.user.email}"


class UserChallenge(models.Model):
    CHALLENGE_CHOICES = [
        ('lack of direction', 'lack of direction'),
        ('inconsistency', 'inconsistency'),
        ('too many resources', 'too many resources'),
        ('lack of practice', 'lack of practice'),
        ('forgetting concepts', 'forgetting concepts'),
    ]

    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.CharField(max_length=50, choices=CHALLENGE_CHOICES)

    def __str__(self):
        return f"{self.challenge} for {self.profile.user.email}"


class IkigaiResponse(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='ikigai_response')
    passion = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    impact = models.JSONField(default=list, blank=True)
    career = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ikigai response for {self.profile.user.email}"


class IkigaiScore(models.Model):
    CAREER_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Full Stack', 'Full Stack'),
        ('Data Science', 'Data Science'),
        ('AI/ML', 'AI/ML'),
    ]

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='ikigai_score')
    frontend_score = models.FloatField(default=0)
    backend_score = models.FloatField(default=0)
    fullstack_score = models.FloatField(default=0)
    data_science_score = models.FloatField(default=0)
    ai_ml_score = models.FloatField(default=0)
    best_fit = models.CharField(max_length=50, choices=CAREER_CHOICES, blank=True)
    result_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ikigai score for {self.profile.user.email}: {self.best_fit}"
class CareerQuizResult(models.Model):

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='career_results'
    )

    recommended_career = models.CharField(max_length=255)

    confidence_score = models.FloatField(default=0)

    career_category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    explanation = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommended_career} for {self.profile.user.email}"