from django.db import models
from django.conf import settings
from django.utils import timezone

class UserAccount(models.Model):
    username = models.CharField(max_length=24, unique=True)
    password = models.CharField(max_length=24)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username
        return self.password
        return self.first_name
        return self.last_name
