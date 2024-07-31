from django.db import models
from category.models import Category


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    done = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
