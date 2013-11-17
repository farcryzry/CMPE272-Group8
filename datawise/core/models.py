from django.db import models

# Create your models here.

class Result(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)