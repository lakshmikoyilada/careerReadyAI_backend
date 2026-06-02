from django.db import models
from django.conf import settings
from django.conf import settings


class CareerRecommendation(models.Model):

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    recommended_career = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.recommended_career}"
    
class SavedCareerRecommendation(models.Model):

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)

    career_name = models.CharField(max_length=255)

    score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.email} - {self.career_name}"