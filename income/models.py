from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=65)
    source = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Income'


class Source(models.Model):
    name = models.CharField(max_length=150)
