from django.db import models
from django.contrib.auth.models import User


# Create your models here
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to="projects")

    def __str__(self):
        return f"Project({self.name}, {self.description}, picture)"


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    def __str__(self):
        return f"Participation({self.user.id}, {self.project.id}, {self.role})"

    class Meta:
        unique_together = ("user", "project")


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()
    completed = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default="default")

    def __str__(self):
        return f"Task({self.name}, {self.description}, {self.start}, {self.end}, {self.completed}, {self.color})"


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Assignments({self.task.id}, {self.user.id})"

    class Meta:
        unique_together = ("task", "user")
