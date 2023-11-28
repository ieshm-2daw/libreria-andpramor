from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

GENEROS = (
    ('fantasia', 'Fantasía'),
    ('no-ficcion', 'No Ficción'),
    ('terror', 'Terror'),
    ('ciencia-ficcion', 'Ciencia Ficción'),
)

DISPONIBILIDAD_VALORES = (
    ('disponible', 'Disponible'),
    ('prestado', 'Prestado'),
    ('en-proceso', 'En proceso de préstamo'),
)

class Usuario(AbstractUser):
    dni = models.CharField(max_length=9)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.BigIntegerField(validators=[validators.MinValueValidator(100000000), validators.MaxValueValidator(999999999)])

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    biografia = models.TextField(max_length=500)
    foto = models.ImageField(upload_to='autores/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    sitio_web = models.URLField()

    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    autores = models.ManyToManyField(Autor)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=20, choices=GENEROS)
    ISBN = models.BigIntegerField(validators=[validators.MinValueValidator(1000000000000), validators.MaxValueValidator(9999999999999)]) #El ISBN es un número de 13 cifras.
    resumen = models.TextField(max_length=500)
    disponibilidad = models.CharField(max_length=30, choices=DISPONIBILIDAD_VALORES)
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Préstamo:
    ESTADO_CHOICES = (
        ('prestado','Prestado'),
        ('devuelto','Devuelto',)
    )
    libro_prestado = models.ForeignKey(Libro, on_delete=models.SET_NULL)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True,blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL)
    estado_prestamo = models.CharField(max_length=20, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.usuario