from django.db import models

#class Usuario(models.Model): #Hacer este con AbstractUser
    #atributos
    #metodos

class Libro(models.Model):
    titulo = models.CharField(max_length=50)
    autores = models.CharField()
    editorial
    fecha_publicacion
    genero
    ISBN
    resumen
    disponibilidad
    portada

    def __str__(self):
        return self.titulo