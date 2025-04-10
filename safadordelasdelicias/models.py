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
    CATEGORIA = [

    ]

    id_Producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
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
    id_pedido = models.AutoField(primary_key=True)
    id_mesa = models.ForeignKey(Mesa, on_delete=models.DO_NOTHING)
    estado = models.CharField(max_length=20, choices=EstadoPedido, default=EstadoPedido.pendiente)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"


class LineaPedido(models.Model):
    id_linea_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, related_name='lineas')
    id_producto = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    cantidad_producto = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Línea {self.id} - {self.id_producto.nombre} x{self.cantidad_producto}"


class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    salario = models.FloatField()
    horas_semanales = models.PositiveIntegerField()
    dias_vacaciones = models.PositiveIntegerField()
    horas_extra = models.PositiveIntegerField()
    faltas = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()

    def __str__(self):
        return f"Contrato {self.id_contrato}"


class Empleados(models.Model):
    SEXO = [('',''),('',''),('','')]

    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100,choices=SEXO, default='Otro')
    puesto = models.CharField(max_length=100)
    cuenta_bancaria = models.CharField(max_length=100)
    id_contrato = models.ForeignKey(Contratos, on_delete=models.RESTRICT)