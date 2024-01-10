from datetime import date
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Libro, Prestamo, Autor, Editorial
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ListViewLibros(ListView): #LISTA
    model = Libro
    template_name = 'libreria/lista_libros.html'

    #Por un lado, monto el contexto que voy a pasarle a la plantilla. Necesito libros disponibles y prestados, autores con los que filtrar y si llego desde el formulario en lugar de desde el enlace, necesito el autor seleccionado.    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Así lo hacía antes del filtro:
        # context['libros_disponibles'] = Libro.objects.filter(disponibilidad='disponible')
        # context['libros_prestados'] = Libro.objects.filter(disponibilidad='prestado')
        # Para aplicar el filtro, en lugar de coger los libros de la base de datos, tenemos que coger los libros que devuelve el filtro:
        queryset = self.get_queryset()
        context['libros_disponibles'] = queryset.filter(disponibilidad='disponible')
        context['libros_prestados'] = queryset.filter(disponibilidad='prestado')
        context['autores'] = Autor.objects.all()
        context['editoriales'] = Editorial.objects.all()
        context['autor_seleccionado'] = self.request.GET.get('autor') #autor es como he llamado el campo select del formulario de la template, metiendo esto en el contexto puedo hacer que al usar el filtro, en el formulario salga seleccionado el autor que había usado para filtrar en lugar de que muestre de nuevo "Todos los autores".
        context['editorial_seleccionada'] = self.request.GET.get('editorial')
        return context
    
    #Ahora definimos el conjunto de objetos que va a llegar a la template, el queryset, según el formulario del template, es decir, redefinimos el queryset según el filtro de autores.
    def get_queryset(self) -> QuerySet[Any]:
        #return super().get_queryset() Este es el get_queryset por defecto, que es el que devolveré al llegar a la template sin usar el formulario de filtrado de autor.
        queryset = super().get_queryset()
        autor = self.request.GET.get('autor') #Si llegamos desde el formulario, tendremos un valor en autor, así que guardamos su nombre para filtrar ahora.
        editorial = self.request.GET.get('editorial')
        if autor: #Si existe autor:
            queryset = queryset.filter(autores__nombre__icontains=autor) #Este filtro busca en cada libro del queryset si el campo autores (autores__nombre) tiene al menos un resultado (__icontains) que coincida con el autor seleccionado
        if editorial:
            queryset = queryset.filter(editorial__nombre=editorial)
        return queryset #Si he filtrado, el queryset que devuelvo es el filtrado, sino, es el que devolvería por defecto.


class CreateViewLibro(LoginRequiredMixin, CreateView): #CREATE
    model = Libro
    fields = ['titulo','autores','editorial','fecha_publicacion','genero','ISBN','resumen','disponibilidad','portada']
    template_name = 'libreria/nuevo_libro.html'
    success_url = reverse_lazy('lista_libros')

class DetailViewLibro(DetailView): #READ
    model = Libro
    template_name = 'libreria/detalle_libro.html'

class UpdateViewLibro(LoginRequiredMixin, UpdateView): #UPDATE
    model = Libro
    fields = ['titulo','autores','editorial','fecha_publicacion','genero','ISBN','resumen','disponibilidad','portada']
    template_name = 'libreria/editar_libro.html'
    success_url = reverse_lazy('lista_libros')

class DeleteViewLibro(LoginRequiredMixin, DeleteView): #DELETE
    model = Libro
    template_name = 'libreria/eliminar_libro.html'
    success_url = reverse_lazy('lista_libros')

class PrestamoLibro(LoginRequiredMixin, View):
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
    
class DevolucionLibro(LoginRequiredMixin, View):
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