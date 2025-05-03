from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

# Clase para los usuarios
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=settings.ROLES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.usuario.username + ' - ' + self.rol

# Modelo Base para Productos (Abstracto)
class Producto(models.Model):
    nombre = models.CharField(max_length=100, default='Nombre')
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre

# Clase para las Versiones (Hereda de Producto)
class Version(Producto):
    id_version = models.AutoField(primary_key=True)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='versiones/', null=True, blank=True)

    def __str__(self):
        return f"Versión: {self.nombre}"

# Modelo Base para Extensiones (Hereda de Producto, Abstracto)
class Extension(Producto):
    class Meta:
        abstract = True

    def __str__(self):
        return f"Extensión: {self.nombre}"

# Subclase para Skins (Hereda de Extension)
class Skins(Extension):
    FACTION_CHOICES = [
        ('bear', 'BEAR'),
        ('usec', 'USEC'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='skins/', null=True, blank=True)
    facción = models.CharField(
        max_length=4,
        choices=FACTION_CHOICES,
        default='BEAR',
    )

    class Meta:
        verbose_name = "Skins"
        verbose_name_plural = "Skins"

    def __str__(self):
        return f"Skin: {self.nombre} ({self.get_facción_display()})"

# Subclase para PVE (Hereda de Extension)
class Pve(Extension):
    pass

    class Meta:
        verbose_name = "PvE"
        verbose_name_plural = "PvE"

    def __str__(self):
        return f"PvE: {self.nombre}"

# Subclase para Agrandar Alijo (Hereda de Extension)
class AgrandarAlijo(Extension):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='alijos/', null=True, blank=True)

    def __str__(self):
        return f"Agrandar Alijo: {self.nombre}"
    
class Ticket(models.Model):
    ESTADOS = (
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('cerrado', 'Cerrado'),
    )

    prioridades = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='abierto')
    prioridad = models.CharField(max_length=10, choices=prioridades, default='media')

    def __str__(self):
        return f"Ticket #{self.id} - {self.asunto} ({self.usuario.username})"