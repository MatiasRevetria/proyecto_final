from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 

# Create your views here.
def login_user(request):
    return render(request,'log_base.html',{'form':UserCreationForm})
