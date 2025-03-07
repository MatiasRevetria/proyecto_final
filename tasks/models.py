from django.db import models
from user_login.models import *

# Create your models here.
class Receta(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.name
    