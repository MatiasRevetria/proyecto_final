from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView 
from django.http import HttpResponse,JsonResponse
from .models import Receta
from user_login.models import Usuario
from .forms import RecetaNueva



# Create your views here.
def main_page(request):
    title = 'Django-course'
    recetas = Receta.objects.all()
    return render(request,'main.html',{
        'title': title,
        'recetas': recetas,
    })

def logout_user(request):
    try:
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('/login/')

#def recetas(request,id):
    #recetas = list(Receta.objects.values())
    #return JsonResponse(receta, safe=False)
    #receta = Receta.objects.get(id=id)
#   receta = get_object_or_404(Receta,id=id)
#   return HttpResponse('receta: %s' % receta.title)

def recetas(request):
    recetas = Receta.objects.all()
    return render(request,'recetas.html',{'recetas':recetas})

def favoritas(request):
    return HttpResponse('Hello world!')

def crear_receta(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'GET':
        return render(request,'create_receta.html',{'form':RecetaNueva()})
    elif request.method == 'POST':
        form = RecetaNueva(request.POST)
        if form.is_valid():
            receta = Receta(title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            coccion=form.cleaned_data['coccion'],
                            user=usuario
                            )
            receta.save()
            return redirect('/recetas/')
        

def editar_receta(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id = usuario_id)
    receta = get_object_or_404(Receta, id=id, user = usuario)

    if request.method == 'GET':
        form = RecetaNueva(initial={
            'title': receta.title,
            'description': receta.description,
            'coccion': receta.coccion
        })
        return render(request, 'create_receta.html', {'form': form, 'receta': receta})
    elif request.method == 'POST':
        form = RecetaNueva(request.POST)
        if form.is_valid():
            receta.title = form.cleaned_data['title']
            receta.description = form.cleaned_data['description']
            receta.coccion = form.cleaned_data['coccion']
            receta.save()
            return redirect('/recetas/')


def eliminar_receta(request, id):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)
    receta = get_object_or_404(Receta, id=id, user=usuario)

    if request.method == 'POST':
        receta.delete()
        return redirect('/recetas/')
    
    return render(request, 'delete_receta.html', {'receta': receta})