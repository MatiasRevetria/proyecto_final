from django.views import View
from django.shortcuts import render, redirect
from .forms import New_user, Old_user
from .models import Usuario
from django.contrib import messages
import re

class RegisterUserView(View):
    template_name = 'new_user.html'

    def get(self, request):
        return render(request, self.template_name, {'form': New_user()})

    def post(self, request):
        form = New_user(request.POST)
        if form.is_valid():
            name = request.POST['name']
            passwd1 = request.POST['passwd']
            passwd2 = request.POST['passwd2']

            if passwd1 != passwd2:
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'Las contraseñas no coinciden.'
                })

            # Validación de complejidad mínima
            if len(passwd1) < 8 or not re.search(r'[A-Z]', passwd1) or not re.search(r'\d', passwd1):
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.'
                })

            if Usuario.objects.filter(name=name).exists():
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'Este usuario ya existe.'
                })

            usuario = Usuario(name=name)
            usuario.set_password(passwd1)
            usuario.save()
            request.session['usuario_id'] = usuario.id
            return redirect('/recetas/')
        
        return render(request, self.template_name, {'form': form})


class LoginUserView(View):
    template_name = 'old_user.html'

    def get(self, request):
        return render(request, self.template_name, {'form': Old_user()})

    def post(self, request):
        name = request.POST['name']
        passwd = request.POST['passwd']

        try:
            usuario = Usuario.objects.get(name=name)
        except Usuario.DoesNotExist:
            return render(request, self.template_name, {
                'form': Old_user(),
                'error': 'Usuario no encontrado'
            })

        if usuario.check_password(passwd):
            request.session['usuario_id'] = usuario.id
            return redirect('/recetas/')
        else:
            return render(request, self.template_name, {
                'form': Old_user(),
                'error': 'Contraseña incorrecta'
            })


class LandingPageView(View):
    def get(self, request):
        return render(request, 'landing_page.html')
