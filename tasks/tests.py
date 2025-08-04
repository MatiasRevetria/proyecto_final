from django.test import TestCase, Client
from django.urls import reverse
from user_login.models import Usuario
from tasks.models import Receta

class UsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(name='matias', passwd='1234')
    
    def test_login_exitoso(self):
        response = self.client.post('/login/', {
            'name': 'matias',
            'passwd': '1234'
        })
        self.assertEqual(response.status_code, 302)  # Redirecciona
        self.assertIn('usuario_id', self.client.session)

    def test_login_fallido(self):
        response = self.client.post('/login/', {
            'name': 'matias',
            'passwd': 'wrongpass'
        })
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_crear_usuario(self):
        response = self.client.post('/register/', {
            'name': 'nuevo',
            'passwd': 'abc',
            'passwd2': 'abc'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(name='nuevo').exists())

class RecetaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(name='matias', passwd='1234')
        self.client.session['usuario_id'] = self.usuario.id
        self.client.session.save()

    def test_crear_receta(self):
        response = self.client.post('/nueva/', {
            'title': 'Tarta',
            'description': 'Muy rica',
            'coccion': 30,
            'dificultad': 'Facil',
            'categoria': 'Cena',
        })
        self.assertEqual(response.status_code, 200)  # o 302 si redirige


