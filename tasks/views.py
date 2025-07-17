
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, TemplateView, RedirectView
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .models import Receta, Comentario, Valoracion
from user_login.models import Usuario
from .forms import RecetaNueva, ComentarReceta


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
        return render(request, self.template_name, {
            'recetas': recetas,
            'usuario_id': usuario_id,
            'forms_dict': forms_dict,
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
        receta = get_object_or_404(Receta, id=receta_id)
        receta.favs = True
        receta.save()
        return redirect('/recetas/')


class DesmarcarFavoritaView(View):
    def get(self, request, receta_id):
        receta = get_object_or_404(Receta, id=receta_id)
        receta.favs = False
        receta.save()
        return redirect('/recetas/')


class FavoritasView(TemplateView):
    template_name = 'favoritas.html'


class CrearRecetaView(CreateView):
    model = Receta
    form_class = RecetaNueva
    template_name = 'create_receta.html'
    success_url = reverse_lazy('recetas')

    def form_valid(self, form):
        usuario_id = self.request.session.get('usuario_id')
        form.instance.user = Usuario.objects.get(id=usuario_id)
        return super().form_valid(form)


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
