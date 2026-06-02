from django.db import models
from django.conf import settings


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    education = models.CharField(
        max_length=100,
        blank=True
    )

    specialization = models.CharField(
        max_length=100,
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    interests = models.TextField(
        blank=True
    )

    is_profile_complete = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.email