from django.db import models


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
    ESTADOS_MESA = [
        ('libre', 'Libre'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADOS_MESA, default='libre')

    def __str__(self):
        return f"Mesa {self.id} - {self.estado}"


class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    id_mesa = models.ForeignKey(Mesa, on_delete=models.RESTRICT)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"


class LineaPedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    id_producto = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    cantidad_producto = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Línea {self.id} - {self.id_producto.nombre} x{self.cantidad_producto}"