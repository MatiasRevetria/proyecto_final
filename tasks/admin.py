from django.contrib import admin
from .models import Receta
from user_login.models import Usuario
# Register your models here.

admin.site.register(Receta)
admin.site.register(Usuario)