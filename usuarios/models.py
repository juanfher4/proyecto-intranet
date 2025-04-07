import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.urls import reverse

""" 
# Creo una variable y le indico que es donde se van a almacenar las fotos, en la carpeta 'media'
static_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'media'))
 """
class Rol(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'])
        ]

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('usuarios:profile_list_rol',
                       args=[self.slug])

class Profile(models.Model):
    roles = models.ManyToManyField(Rol,
                            related_name='profiles',
                            blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    imagen = models.ImageField(upload_to='users/%Y/%m/%d',
                               blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
