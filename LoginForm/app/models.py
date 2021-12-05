from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(verbose_name='Address', max_length=50, default="Unknown address")

    def __str__(self):
        return self.user.username
