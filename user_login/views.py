from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import Usuario

# Create your views here.ç¨´
def create_user(request):
    if request.method == 'GET':
        return render(request,'new_user.html',{'form': New_user()})
    else:
        if request.POST['passwd'] == request.POST['passwd2']:
            Usuario.objects.create(name=request.POST['name'],passwd=request.POST['passwd'])
            return redirect('/home/')
        else:
            return render(request,'new_user.html',{'form': New_user(),'error': 'Passwords do not match'})
        
def login_user(request):
    if request.method == 'GET':
        return render(request, 'old_user.html', {'form': Old_user()})
    else:
        name = request.POST['name']
        passwd = request.POST['passwd']

        users = Usuario.objects.filter(name=name, passwd=passwd)
        
        if users.exists():
            user = users.first()  
            request.session['usuario_id'] = user.id
            return redirect('/home/')
        else:
            return render(request, 'old_user.html', {
                'form': Old_user(),
                'error': 'Usuario o contraseña incorrectos'
            })


            
def landing_page(request):
    return render(request,'landing_page.html')
        
