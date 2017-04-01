from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Site(models.Model):
    title = models.CharField(max_length=200)
    test = models.TextField()
    user = models.ForeignKey(User)

    #  @property
    # @property
    def __str__(self):
        return self.title
