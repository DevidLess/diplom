from django.db import models


# Create your models here.
class TestDB(models.Model):
    first = models.CharField(max_length=256)
    second = models.CharField(max_length=256)
    third = models.CharField(max_length=256)
    fourth = models.CharField(max_length=256)
