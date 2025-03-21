from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from .forms import *
from .models import Usuario

# Create your views here.
def login_user(request):
    return render(request,'log_base.html',{'form':UserCreationForm})

def create_user(request):
    if request.method == 'GET':
        return render(request,'new_user.html',{'form': New_user()})
    else:
        Usuario.objects.create(name=request.POST['name'],passwd=request.POST['passwd'])
        return redirect('home/')
        