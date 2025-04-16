from django.db import models

# Create your models here.

# Clase para los usuarios
class Usuario(models.Model):       #Considerando usar AbastractUser
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=15, choices=TIPOS_USUARIO, default='cliente')

    def __str__(self):
        return self.nombre

# Clase para las versiones
class Version(models.Model):
    id_version = models.AutoField(primary_key=True)
    nombre_version = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    caracteristicas = models.TextField()
    activo = models.BooleanField(default=True) #Para quitar o poner versiones

    def __str__(self):
        return self.nombre_version
    
# Clase base para las extensiones (abstracta)    
class BaseExtension(models.Model):
    TIPOS_EXTENSION = [
        ('inventario', 'Agrandar Inventario'),
        ('skin', 'Skin'),
        ('pve', 'PvE'),
    ]
    nombre_extension = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True #No genera una tabla en la base de datos

    def __str__(self):
        return self.nombre_extension
    
# Subclase para extensiones de inventario
class InvExtension(BaseExtension):
    inv_extra = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre_extension} (Inventario)"
    
# Subclase para skins BEAR
class BearSkinExtension(BaseExtension):
    skin = models.CharField(default= 'BEAR', max_length=25)

    def __str__(self):
        return f"{self.nombre_extension} (BEAR)"
    
# Subclase para skins USEC
class UsecSkinExtension(BaseExtension):
    skin = models.CharField(default= 'USEC', max_length=25)

    def __str__(self):
        return f"{self.nombre_extension} (USEC)"
    
# Subclase para el PVE
class PveExtension(BaseExtension):
    def __str__(self):
        return f"{self.nombre_extension} (BEAR)"