import secrets
import string

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class EstadoMesa(models.TextChoices):
    disponible = 'Disponible'
    en_curso = 'En Curso'


class Puesto_trabajo(models.TextChoices):
    camarero = 'Camarero'
    cocinero = 'Cocinero'
    administrador = 'Administrador'


class Tipo_contrato(models.TextChoices):
    indefinido = 'Indefinido'
    fijo_discontinuo = 'Fijo discontinuo'
    tiempo_parcial_15 = 'Tiempo Parcial 15h'
    tiempo_parcial_20 = 'Tiempo Parcial 20h'


class EstadoPedido(models.TextChoices):
    pendiente = 'Pendiente'
    en_proceso = 'En Proceso'
    completado = 'Completado'
    cancelado = 'Cancelado'
    en_retraso = 'En Retraso'


class CategoriaProducto(models.TextChoices):
    comida = 'Comida'
    bebida = 'Bebida'


class TipoCategoria(models.TextChoices):
    entrantes = 'Entrantes'
    platos = 'Platos'
    revueltos = 'Revueltos'
    verduras = 'Verduras'


class SubCategoria(models.TextChoices):
    carne = 'Carne'
    pescado = 'Pescado'
    arroz = 'Arroz'


class SEXO(models.TextChoices):
    femenino = 'F'
    masculino = 'M'
    otros = 'O'


class Mesa(models.Model):
    estado = models.CharField(max_length=20, choices=EstadoMesa, default=EstadoMesa.disponible)

    def __str__(self):
        return f"Mesa {self.id} - {self.estado}"


class Contratos(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    tipo_contrato = models.CharField(choices=Tipo_contrato, default=Tipo_contrato.indefinido, max_length=20)
    salario = models.FloatField(null=True)
    horas_semanales = models.PositiveIntegerField(null=True)
    dias_vacaciones = models.PositiveIntegerField(null=True)
    horas_extra = models.PositiveIntegerField(null=True)
    faltas = models.PositiveIntegerField(null=True)
    mes = models.PositiveIntegerField(null=True)
    fecha_alta = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    numero_seguridad_social = models.CharField(max_length=100, null=True)
    cuenta_bancaria = models.CharField(max_length=100)

    def __str__(self):
        return f"Contrato {self.tipo_contrato}"


class UsuarioManager(BaseUserManager):

    def generar_contrasenia(longitud=6):
        return ''.join(secrets.choice(string.digits) for _ in range(longitud))
    def create_user(self, correo, nombre, puesto, password=None):

        if not correo:
            raise ValueError("El usuario debe tener un email")
        correo = self.normalize_email(correo)
        empleado = self.model(correo=correo, nombre=nombre, puesto=puesto)

        if password is None:
            password = self.generar_contrasenia()

        empleado.set_password(password)
        empleado.save(using=self._db)
        return empleado

    def create_superuser(self, email, nombre, rol='admin', password=None):
        empleado = self.create_user(email, nombre, rol, password)
        empleado.is_superuser = True
        empleado.is_staff = True
        empleado.save(using=self._db)
        return empleado


class Empleados(AbstractBaseUser, PermissionsMixin):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(null=True)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=100)
    dni = models.CharField(max_length=100, unique=True)
    sexo = models.CharField(max_length=100, choices=SEXO, default=SEXO.otros)
    id_contrato = models.ForeignKey(Contratos, on_delete=models.RESTRICT, null=True, blank=True)
    fecha_alta = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    puesto = models.CharField(max_length=100, choices=Puesto_trabajo, default=Puesto_trabajo.camarero)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=100,default='<PASSWORD>')
    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return f"Empleado {self.id_empleado}"

class Productos(models.Model):
    id_Producto = models.AutoField(primary_key=True, default=1)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.CharField(max_length=100, choices=CategoriaProducto, default=CategoriaProducto.comida)
    tipo_categoria = models.CharField(max_length=100, choices=TipoCategoria, default=TipoCategoria.platos, null=True)
    disponibilidad = models.BooleanField(default=True)
    subcategoria = models.CharField(max_length=100, default='', null=True, choices=SubCategoria)
    stock = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_mesa = models.ForeignKey(Mesa, on_delete=models.DO_NOTHING)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.DO_NOTHING, null=True, blank=True)
    cerrado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.id_pedido} - Cerrado: {self.cerrado}"


class LineaPedido(models.Model):
    id_linea_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, related_name='lineas')
    id_producto = models.ForeignKey(Productos, on_delete=models.RESTRICT)
    cantidad_producto = models.PositiveIntegerField(default=1)
    fecha_alta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=EstadoPedido, default=EstadoPedido.pendiente)

    def __str__(self):
        return f"Línea {self.id_linea_pedido} - {self.id_producto.nombre} x{self.cantidad_producto}"
