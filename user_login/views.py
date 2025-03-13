from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from .forms import *

# Create your views here.
def login_user(request):
    return render(request,'log_base.html',{'form':UserCreationForm})

def create_user(request):
    return render(request,'new_user.html',{'form': New_user})
