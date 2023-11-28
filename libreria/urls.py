from django.urls import path
from .views import *

urlpatterns = [
    path('',ListViewLibros.as_view(),name='lista_libros'),
    path('nuevo_libro/',CreateViewLibro.as_view(),name='nuevo_libro'),
    path('detalle_libro/<int:pk>',DetailViewLibro.as_view(),name='detalle_libro'),
    path('editar_libro/<int:pk>',UpdateViewLibro.as_view(),name='editar_libro'),
    path('eliminar_libro/<int:pk>',DeleteViewLibro.as_view(),name='eliminar_libro'),
]