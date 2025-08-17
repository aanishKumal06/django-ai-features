from django.db import models

# Create your models here.
class Advice(models.Model):
    problem = models.TextField()
    medicines = models.TextField()

    class Meta:
        verbose_name = "Advice"
        verbose_name_plural = "Advices"