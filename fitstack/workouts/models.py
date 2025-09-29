from django.db import models
class WorkoutSession(models.Model):
    title = models.CharField(max_length=100)
    duration_min = models.FloatField()

    def __str__(self):
        return f"{self.title} ({self.duration_min} min)"