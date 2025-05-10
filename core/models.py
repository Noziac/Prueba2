from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

User = get_user_model()

# Clase para los usuarios
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=settings.ROLES, default='cliente')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except PerfilUsuario.DoesNotExist:
        PerfilUsuario.objects.create(usuario=instance)

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

# Clase para comprar productos
class Compra(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    resena_hecha = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha_compra']

    def __str__(self):
        return f"Compra de {self.content_object} por {self.usuario.username} el {self.fecha_compra}"
    
# Clase para reseñas
class Resena(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    texto = models.TextField()
    evaluacion = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE, null=True, blank=True, related_name='mi_reseña')

    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.content_object}"