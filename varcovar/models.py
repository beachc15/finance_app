from django.db import models

# Create your models here.
from django.db import models
from django_pandas.managers import DataFrameManager


class Product(models.Model):
    product_name = models.TextField()
    objects = models.Manager()
    pdobjects = DataFrameManager()  # Pandas-Enabled Manager

