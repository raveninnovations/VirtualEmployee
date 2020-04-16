from django.db import models

# Create your models here.

class register(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return str(self.name) if self.name else ''