from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    muscle_group = models.CharField(max_length=100, db_index=True)
    equipment = models.JSONField(default=list)
    image_url = models.URLField()

    def __str__(self):
        return self.name