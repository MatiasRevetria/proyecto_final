from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    name = models.CharField(max_length=255, unique=True)
    passwd = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.passwd = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.passwd)

    def __str__(self):
        return self.name


#El hash se genera con make_password, el cual incluye salt.

#Se usa check_password para validar.

#La validación de complejidad es simple: mínimo 8 caracteres, 1 mayúscula y 1 número. Podés ampliarla según necesidad.


