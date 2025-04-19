from django.contrib import admin

# Register your models here.
from .models import Usuario, Version

admin.site.register(Usuario)
admin.site.register(Version)