from django.db import models
from django.contrib.auth.models import User

# Create your models here


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="projects")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
