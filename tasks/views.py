
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .models import Receta, Comentario, Valoracion, RecetaFavorita
from user_login.models import Usuario
from .forms import RecetaNueva, ComentarReceta, RecetaIngrediente, RecetaIngredienteFormSet


class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Django-course'
        context['recetas'] = Receta.objects.all()
        return context


class LogoutUserView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        request.session.pop('usuario_id', None)
        return super().get(request, *args, **kwargs)


class RecetaListView(View):
    template_name = 'recetas.html'

    def get(self, request):
        recetas = Receta.objects.all()
        usuario_id = request.session.get('usuario_id')
        forms_dict = {receta.id: ComentarReceta() for receta in recetas}
        favoritas_ids = RecetaFavorita.objects.filter(user_id=usuario_id).values_list('receta_id', flat=True)

        return render(request, self.template_name, {
            'recetas': recetas,
            'usuario_id': usuario_id,
            'forms_dict': forms_dict,
            'favoritas_ids': list(favoritas_ids),
        })

    def post(self, request):
        form = ComentarReceta(request.POST)
        receta_id = request.POST.get('receta_id')
        usuario_id = request.session.get('usuario_id')
        if form.is_valid() and usuario_id and receta_id:
            comentario = form.save(commit=False)
            comentario.user = Usuario.objects.get(id=usuario_id)
            comentario.receta = Receta.objects.get(id=receta_id)
            comentario.save()
        return redirect('/recetas/')


class MisRecetasView(ListView):
    template_name = 'mis_recetas.html'
    context_object_name = 'recetas'

    def get_queryset(self):
        usuario_id = self.request.session.get('usuario_id')
        if not usuario_id:
            return Receta.objects.none()
        return Receta.objects.filter(user_id=usuario_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['recetas']:
            context['mensaje'] = 'No tienes recetas creadas'
        return context


class MarcarCocinadaView(View):
    def get(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        receta.cooked = True
        receta.save()
        return redirect('/recetas/')


class DesmarcarCocinadaView(View):
    def get(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        receta.cooked = False
        receta.save()
        return redirect('/recetas/')


class MarcarFavoritaView(View):
    def get(self, request, receta_id):
        usuario_id = request.session.get('usuario_id')
        if usuario_id:
            receta = get_object_or_404(Receta, id=receta_id)
            user = get_object_or_404(Usuario,id=usuario_id)
            RecetaFavorita.objects.get_or_create(user=user, receta=receta)
        return redirect('/recetas/')


class DesmarcarFavoritaView(View):
    def get(self, request, receta_id):
        usuario_id = request.session.get('usuario_id')
        if usuario_id:
            receta = get_object_or_404(Receta, id = receta_id)
            user = get_object_or_404(Usuario,id = usuario_id)
            RecetaFavorita.objects.filter(user=user, receta=receta).delete()
        return redirect('/recetas/')


class FavoritasView(ListView):
    template_name = 'favorites.html'
    context_object_name = 'favoritas'

    def get_queryset(self):
        usuario_id = self.request.session.get('usuario_id')
        if not usuario_id:
            return Receta.objects.none()
        return Receta.objects.filter(id__in=RecetaFavorita.objects.filter(user_id=usuario_id).values_list('receta_id', flat=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['favoritas']:
            context['mensaje'] = 'No tienes recetas favoritas'
        return context
        



class CrearRecetaView(CreateView):
    template_name = 'create_receta.html'

    def get(self, request):
        receta_form = RecetaNueva()
        ingrediente_formSet = RecetaIngredienteFormSet(queryset=RecetaIngrediente.objects.none())
        return render(request, self.template_name, {'form':receta_form, 'ingredientes':ingrediente_formSet})

    def post(self, request,):
        receta_form = RecetaNueva(request.POST, request.FILES)
        ingrediente_formset = RecetaIngredienteFormSet(request.POST)

        if receta_form.is_valid() and ingrediente_formset.is_valid():
            usuario_id = request.session.get('usuario_id')
            receta = receta_form.save(commit=False)
            receta.user = Usuario.objects.get(id=usuario_id)
            receta.save()

            ingredientes = ingrediente_formset.save(commit=False)
            for ing in ingredientes:
                ing.receta = receta
                ing.save()
        
            return redirect('recetas')
        return render( request, self.template_name, {'form': receta_form, 'ingredientes': ingrediente_formset})
    

class EditarRecetaView(UpdateView):
    model = Receta
    form_class = RecetaNueva
    template_name = 'edit_receta.html'
    success_url = reverse_lazy('recetas')


class EliminarRecetaView(DeleteView):
    model = Receta
    template_name = 'delete_receta.html'
    success_url = reverse_lazy('recetas')


class ValorarRecetaView(View):
    def post(self, request, receta_id):
        usuario_id = request.session.get("usuario_id")
        puntaje = request.POST.get("puntaje")

        if not usuario_id or not puntaje:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

        receta = Receta.objects.get(id=receta_id)
        usuario = Usuario.objects.get(id=usuario_id)

        valoracion, created = Valoracion.objects.update_or_create(
            receta=receta,
            user=usuario,
            defaults={"puntaje": puntaje}
        )
        return redirect('/recetas/')
