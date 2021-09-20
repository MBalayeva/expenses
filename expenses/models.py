from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=65)
    category = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "categories"
