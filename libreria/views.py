from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Libro
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView #Lista y CRUD

class ListViewLibros(ListView): #LISTA
    model = Libro
    queryset=Libro.objects.filter(disponibilidad='disponible')
    template_name = 'libreria/lista_libros.html'

class CreateViewLibro(CreateView): #CREATE
    model = Libro
    fields = ['titulo','autores','editorial','fecha_publicacion','genero','ISBN','resumen','disponibilidad','portada']
    template_name = 'libreria/nuevo_libro.html'
    success_url = reverse_lazy('lista_libros')

class DetailViewLibro(DetailView): #READ
    model = Libro
    template_name = 'libreria/detalle_libro.html'

class UpdateViewLibro(UpdateView): #UPDATE
    model = Libro
    fields = ['titulo','autores','editorial','fecha_publicacion','genero','ISBN','resumen','disponibilidad','portada']
    template_name = 'libreria/editar_libro.html'
    success_url = reverse_lazy('lista_libros')

class DeleteViewLibro(DeleteView): #DELETE
    model = Libro
    template_name = 'libreria/eliminar_libro.html'
    success_url = reverse_lazy('lista_libros')