# PROYECTO FINAL

## Requisitos

Facultad de Ingenieria del ejercito
Paradigmas de programacion V
Enunciado:
Desarrollar un sistema de gestión de recetas de cocina, donde los usuarios puedan registrar,
organizar y compartir sus recetas. El sistema permitirá buscar recetas por categorías y
dificultad, además de crear listas de compras con los ingredientes necesarios. Se deben aplicar
los conceptos de Programación Orientada a Objetos (POO), persistencia de datos, pruebas
(tests) y el patrón Modelo-Vista-Template (MVT) de Django.
Requisitos generales:

● El sistema debe ser implementado en Django siguiendo las buenas prácticas de
desarrollo.

● Se deben utilizar clases y conceptos de POO para organizar el código.

● La persistencia de datos se realizará a través de un sistema de base de datos
relacional.

● Se deben escribir pruebas (tests) para verificar el funcionamiento correcto del sistema.

● Aplicar el patrón Modelo-Vista-Template (MVT) de Django correctamente.

### Requisitos del sistema:
1. Registro y Organización de Recetas:
○ Los usuarios podrán registrar nuevas recetas con campos como título,
descripción, ingredientes, pasos de preparación, tiempo de cocción y dificultad.
○ Cada receta deberá tener una categoría (por ejemplo: desayuno, almuerzo,
cena, postre).
○ Los usuarios deben poder visualizar y editar sus propias recetas.
2. Categorización y Búsqueda:
○ Los usuarios podrán buscar recetas usando palabras clave (título o ingrediente).
○ Además, podrán filtrar las recetas por categorías o nivel de dificultad.
3. Carga de Imágenes:
○ Los usuarios podrán añadir imágenes relacionadas con la receta (por ejemplo,
una foto del plato terminado).
○ Las imágenes asociadas a cada receta deben ser visibles dentro del sistema.
4. Valoración y Comentarios:
○ Los usuarios tendrán la opción de valorar recetas mediante un sistema de
estrellas (de 1 a 5).
○ También podrán dejar comentarios en las recetas para compartir sugerencias o
variaciones.
5. Lista de Compras:
○ Los usuarios podrán generar una lista de compras automática con los
ingredientes necesarios para una o varias recetas seleccionadas. (Opcional,
integrar con sistema para mandar la lista por mail).
Facultad de Ingenieria del ejercito
Paradigmas de programacion V
○ La lista de compras se podrá marcar como comprada, vaciándose
automáticamente para futuras compras.
6. Recetas Favoritas:
○ Los usuarios podrán marcar sus recetas favoritas para tener acceso rápido a
ellas.
○ Habrá una sección dedicada para que los usuarios visualicen todas sus recetas
favoritas.
7. Historial de Cocinados:
○ El sistema llevará un registro de cuándo el usuario ha cocinado una receta (de
forma opcional, el usuario podrá registrar esta información).
○ Los usuarios podrán ver un historial de las recetas que han cocinado.
8. Estadísticas y Reportes (Opcional):
○ Los usuarios tendrán acceso a estadísticas sobre sus recetas más cocinadas,
categorías más populares, entre otros datos.
○ Será posible exportar estas estadísticas en formato CSV.
9. Notificaciones (Opcional):
○ Los usuarios recibirán notificaciones cuando alguien valore o comente en una de
sus recetas.
10. Autenticación y Seguridad:
○ Los usuarios deberán iniciar sesión para acceder al sistema.
○ Las contraseñas se almacenarán en forma de hashes y deberán cumplir con
ciertos requisitos de complejidad.


## Docker

### Construir la imagen y ejecutar

```bash
docker-compose up --build
```

### Iniciar aplicacion
```bash
http://localhost:8080/
```