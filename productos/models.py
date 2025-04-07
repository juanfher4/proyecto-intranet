from django.db import models
from usuarios.models import Profile

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    fecha_contacto = models.DateField()
    estado = models.BooleanField(default=True)
    comercial = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'comercial'},
        help_text='El rol debe ser "comercial"'
    )

    def __str__(self):
        return self.nombre