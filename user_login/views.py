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
    users = Usuario.objects.all()
    if request.method == 'GET':
        return render(request,'old_user.html',{'form': Old_user()})
    else:
        for user in users:
            if request.POST['name'] == user.name:
                return redirect('/home/')
            else:
                return render(request,'old_user.html',{'form':Old_user(),'error':'User or Password incorrect'})
        
