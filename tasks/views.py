from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView 
from django.http import HttpResponse,JsonResponse
from .models import Receta, Comentario, Valoracion, VALORACION
from user_login.models import Usuario
from .forms import RecetaNueva,RecetaIngrediente, RecetaIngredienteFormSet, ComentarReceta



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

def recetas(request):
    recetas = Receta.objects.all()
    usuario_id = request.session.get('usuario_id')
    
    # 1. Inicializar formularios por receta
    forms_dict = {receta.id: ComentarReceta() for receta in recetas}

    # 2. Procesar POST
    if request.method == 'POST':
        form = ComentarReceta(request.POST)
        receta_id = request.POST.get('receta_id')
        if form.is_valid() and usuario_id and receta_id:
            comentario = form.save(commit=False)
            comentario.user = Usuario.objects.get(id=usuario_id)
            comentario.receta = Receta.objects.get(id=receta_id)
            comentario.save()
            return redirect('/recetas/')

    return render(request, 'recetas.html', {
        'recetas': recetas,
        'usuario_id': usuario_id,
        'forms_dict': forms_dict,
    })

def mis_recetas(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)
    recetas = Receta.objects.filter(user=usuario)
    if not recetas:
        return render(request, 'mis_recetas.html', {'recetas': recetas, 'mensaje': 'No tienes recetas creadas'})
    return render(request, 'mis_recetas.html', {'recetas': recetas})

def marcar_cocinada(request,receta_id):
    receta = get_object_or_404(Receta, id = receta_id)
    receta.cooked = True
    receta.save()
    return redirect('/recetas/')

def desmarcar_cocinada(request,receta_id):
    receta = get_object_or_404(Receta,id = receta_id)
    receta.cooked = False
    receta.save()
    return redirect('/recetas/')

def marcar_favorita(request, receta_id):
    receta = get_object_or_404(Receta, id = receta_id)
    receta.favs = True
    receta.save()
    return redirect('/recetas/')

def desmarcar_favorita(request, receta_id):
    receta = get_object_or_404(Receta, id = receta_id)
    receta.favs = False
    receta.save()
    return redirect('/recetas/')

def favoritas(request): 
    return HttpResponse('Hello world!')

def crear_receta(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'GET':
        form = RecetaNueva()
        formset = RecetaIngredienteFormSet(queryset=RecetaIngrediente.objects.none())
        return render(request, 'create_receta.html', {'form': form, 'formset': formset})

    elif request.method == 'POST':
        form = RecetaNueva(request.POST, request.FILES)
        formset = RecetaIngredienteFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            receta = form.save(commit=False)
            receta.user = usuario
            receta.save()

            for ing_form in formset:
                if ing_form.cleaned_data:
                    ingrediente = ing_form.save(commit=False)
                    ingrediente.receta = receta
                    ingrediente.save()

            return redirect('/recetas/')
        
        return render(request, 'create_receta.html', {'form': form, 'formset': formset})

        

def editar_receta(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)
    receta = get_object_or_404(Receta, id=id, user=usuario)

    if request.method == 'GET':
        form = RecetaNueva(instance=receta)
        formset = RecetaIngredienteFormSet(queryset=receta.ingredientes.all())
        return render(request, 'edit_receta.html', {
            'form': form,
            'formset': formset,
            'receta': receta
        })

    elif request.method == 'POST':
        form = RecetaNueva(request.POST, request.FILES, instance=receta)
        formset = RecetaIngredienteFormSet(request.POST, queryset=receta.ingredientes.all())

        if form.is_valid() and formset.is_valid():
            form.save()

            # Eliminar todos los ingredientes anteriores
            receta.ingredientes.all().delete()

            # Crear nuevos ingredientes
            for ing_form in formset:
                if ing_form.cleaned_data and not ing_form.cleaned_data.get('DELETE'):
                    RecetaIngrediente.objects.create(
                        receta=receta,
                        nombre=ing_form.cleaned_data['nombre'],
                        cantidad=ing_form.cleaned_data['cantidad'],
                        unidad=ing_form.cleaned_data['unidad']
                    )

            return redirect('/recetas/')

        else:
            print("ERRORES EN FORMULARIOS")
            print(form.errors)
            print(formset.errors)

        return render(request, 'edit_receta.html', {
            'form': form,
            'formset': formset,
            'receta': receta
        })



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

def valorar_receta(request, receta_id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('/login/')
    
    receta = get_object_or_404(Receta, id=receta_id)
    user = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        puntaje = int(request.POST.get('puntaje'))
        valoracion, created = Valoracion.objects.update_or_create(
            receta=receta,
            user=user,
            defaults={'puntaje': puntaje}
        )
    return redirect('/recetas/')
