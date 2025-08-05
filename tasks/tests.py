from django.test import TestCase, Client
from user_login.models import Usuario
from tasks.models import (
    Receta, RecetaFavorita, RecetaCocinada,
    ListaCompra, ItemListaCompra, RecetaIngrediente
)


class UsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario(name='matias')
        self.usuario.set_password('1234Abcd')
        self.usuario.save()
    
    def test_login_exitoso(self):
        response = self.client.post('/login/', {
            'name': 'matias',
            'passwd': '1234Abcd'
        })
        self.assertEqual(response.status_code, 302)
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
            'passwd': 'Abcd1234',
            'passwd2': 'Abcd1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Usuario.objects.filter(name='nuevo').exists())


class RecetaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario(name='matias')
        self.usuario.set_password('1234Abcd')
        self.usuario.save()

        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

        self.receta = Receta.objects.create(
            user=self.usuario,
            title='Tarta',
            description='Muy rica',
            coccion=30,
            dificultad='Facil',
            categoria='Cena'
        )

        RecetaIngrediente.objects.create(
            receta=self.receta,
            nombre="Harina",
            cantidad=200,
            unidad="g"
        )

    def test_crear_receta(self):
        receta_data = {
            'title': 'Empanadas',
            'description': 'Muy buenas',
            'coccion': 20,
            'dificultad': 'Media',
            'categoria': 'Almuerzo',
            'ingredientes-TOTAL_FORMS': '1',
            'ingredientes-INITIAL_FORMS': '0',
            'ingredientes-MIN_NUM_FORMS': '0',
            'ingredientes-MAX_NUM_FORMS': '1000',
            'ingredientes-0-nombre': 'Carne',
            'ingredientes-0-cantidad': '500',
            'ingredientes-0-unidad': 'g',
        }

        response = self.client.post('/nueva/', receta_data, follow=True)
        self.assertIn(response.status_code, [200, 302])

    def test_recetas_list_view(self):
        response = self.client.get('/recetas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tarta')

    def test_mis_recetas_view(self):
        response = self.client.get('/mis_recetas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tarta')

    def test_cocinadas_view_sin_nada(self):
        response = self.client.get('/cocinadas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tenés recetas cocinadas aún.')

    def test_marcar_y_desmarcar_cocinada(self):
        receta_id = self.receta.id
        response = self.client.get(f'/cocinado/{receta_id}')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecetaCocinada.objects.filter(receta=self.receta, user=self.usuario).exists())

        response = self.client.get(f'/noconinada/{receta_id}')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RecetaCocinada.objects.filter(receta=self.receta, user=self.usuario).exists())

    def test_favoritas_view_sin_nada(self):
        response = self.client.get('/favoritas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No tenés recetas favoritas aún.')

    def test_marcar_y_desmarcar_favorita(self):
        receta_id = self.receta.id
        response = self.client.get(f'/favorita/{receta_id}')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecetaFavorita.objects.filter(receta=self.receta, user=self.usuario).exists())

        response = self.client.get(f'/nofavorita/{receta_id}')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RecetaFavorita.objects.filter(receta=self.receta, user=self.usuario).exists())

    def test_generar_lista_compra_y_marcar_comprada(self):
        self.receta.ingredientes.create(nombre="Harina", cantidad=500, unidad="g")

        response = self.client.post('/generar_lista/', {
            'recetas': [str(self.receta.id)]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ItemListaCompra.objects.filter(lista__user=self.usuario).exists())

        response = self.client.post('/marcar_lista/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ItemListaCompra.objects.filter(lista__user=self.usuario).exists())