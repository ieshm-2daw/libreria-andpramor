from datetime import date
from typing import Any
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Libro, Prestamo
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView #Lista y CRUD
from django.views import View

class ListViewLibros(ListView): #LISTA
    model = Libro
    #queryset = Libro.objects.filter(disponibilidad='disponible')
    template_name = 'libreria/lista_libros.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad='disponible')
        context['libros_prestados'] = Libro.objects.filter(disponibilidad='prestado')
        return context

    #Un filtro, meter en listview todos los libros tal cual está en get, y hacer un post con un form en la template con filtros: autor, género por ejemplo. En el método post en esta clase, vemos qué filtro está activo y filtro los libros del contexto que le voy a pasar a la template. Lo más cómodo es meter en la template un formulario con dos desplegables, de forma que el predefinido sea "Todos" y el resto de campos los valores de CHOICES para géneros y los autores que tenga. ¿Le puedo pasar a la template los autores que tenga en la bbdd para rellenar el desplegable?


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

class PrestamoLibro(View):
    def get(self,request,pk):
        libro = Libro.objects.get(pk=pk)
        return render(request,'libreria/prestar_libro.html',{'libro':libro})

    def post(self,request,pk):
        libro = Libro.objects.get(pk=pk)
        libro.disponibilidad = 'prestado'
        libro.save()
        Prestamo.objects.create(
            libro_prestado = libro,
            fecha_prestamo = date.today(),
            usuario = request.user,
            estado_prestamo = 'prestado'
        )
        return redirect('lista_libros')
    
class DevolucionLibro(View):
    def get(self,request,pk):
        libro = Libro.objects.get(pk=pk)
        return render(request,'libreria/devolver_libro.html',{'libro':libro})

    def post(self,pk):
        libro = Libro.objects.get(pk=pk)
        libro.disponibilidad = 'disponible'
        libro.save()
        prestamo = Prestamo.objects.get(libro_prestado = libro, estado_prestamo = 'prestado')
        prestamo.estado_prestamo = 'devuelto'
        prestamo.fecha_devolucion = date.today()
        prestamo.save()
        return redirect('lista_libros')