from django.db import models

# Create your models here.

class login(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) if self.name else ''