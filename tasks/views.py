from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Receta
from user_login.models import Usuario


# Create your views here.
def main_page(request):
    title = 'Django-course'
    recetas = Receta.objects.all()
    return render(request,'main.html',{
        'title': title,
        'recetas': recetas,
    })

def recetas(request,id):
    #recetas = list(Receta.objects.values())
    #return JsonResponse(receta, safe=False)
    #receta = Receta.objects.get(id=id)
    receta = get_object_or_404(Receta,id=id)
    return HttpResponse('receta: %s' % receta.title)

def favoritas(request):
    pass
    