from django.db import models


GENEROS = (
    ('Fantasía'),
    ('No Ficción'),
    ('Terror'),
    ('Ciencia Ficción'),
)

DISPONIBILIDAD_VALORES = (
    ('Disponible'),
    ('Prestado'),
    ('En proceso de préstamo'),
)

#class Usuario(models.Model): #Hacer este con AbstractUser
    #atributos
    #metodos

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    #autores
    #editorial
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=20, choices=GENEROS)
    ISBN = models.BigIntegerField(validators=[models.validators.MinValueValidator(1000000000000), models.validators.MaxValueValidator(9999999999999)]) #El ISBN es un número de 13 cifras y max_length no se le aplica.
    resumen = models.TextField(max_length=500)
    disponibilidad = models.CharField(max_length=30, choices=DISPONIBILIDAD_VALORES)
    portada = models.ImageField()

    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    biografia = models.TextField(max_length=500)
    foto = models.ImageField()

class Editorial:
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    sitio_web = models.CharField(max_length=100)

class Préstamo:
    #libro_prestado
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    #usuario
    estado_prestamo = models.CharField(max_length=20, choices=('Prestado','Devuelto',))