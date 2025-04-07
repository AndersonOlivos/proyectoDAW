from django.db import models

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    imagen = models.ImageField(max_length=1000)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.estado