from django.db import models

class EstadoMesa(models.TextChoices):
    disponible = 'Disponible'
    en_curso = 'En Curso'

class EstadoPedido(models.TextChoices):
    pendiente = 'Pendiente'
    en_proceso = 'En Proceso'
    completado = 'Completado'
    cancelado = 'Cancelado'
    en_retraso = 'En Retraso'


class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.CharField(max_length=100, default='comida')
    tipo_categoria = models.CharField(max_length=100, default='')
    disponibilidad = models.BooleanField(default=True)
    subcategoria = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.nombre


class Mesa(models.Model):

    estado = models.CharField(max_length=20, choices=EstadoMesa, default=EstadoMesa.disponible)

    def __str__(self):
        return f"Mesa {self.id} - {self.estado}"


class Pedido(models.Model):

    id_mesa = models.ForeignKey(Mesa, on_delete=models.DO_NOTHING)
    estado = models.CharField(max_length=20, choices=EstadoPedido, default=EstadoPedido.pendiente)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"


class LineaPedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, related_name='lineas')
    id_producto = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    cantidad_producto = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Línea {self.id} - {self.id_producto.nombre} x{self.cantidad_producto}"