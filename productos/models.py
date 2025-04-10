from django.db import models
from usuarios.models import Profile

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(unique=True)
    proveedores = models.ManyToManyField(
            Proveedor, 
            related_name="materiales",
            blank=True
        )
    
    def __str__(self):
        return self.nombre
    
ESTADOS_ENVIO = [
    ("listo_envio", "Listo para envío"),
    ("fabricando", "Fabricando"),
    ("pendiente_planos", "Pendiente de confirmar los planos"),
]
    
class EnvioMaterial(models.Model):
    id_envio = models.AutoField(primary_key=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="envios"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name="envios"
    )
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField(blank=True, null=True)
    fecha_llegada_real = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=ESTADOS_ENVIO,
        default="pendiente_planos"
    )
    cantidad = models.IntegerField(default=1)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Envío de {self.material.nombre} de {self.proveedor.nombre}. Estado: {self.get_estado_envio_display()}" # get_estado_envio_display() es un método que crea django a partir de el estado del envío

class Espesor(models.Model):
    id_espesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    revestimiento = models.BooleanField(default=False)

class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Ubicación ({self.latitud}, {self.longitud})"

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    num_habitaciones = models.IntegerField()
    num_banios = models.IntegerField()
    num_plantas = models.IntegerField()
    pared_m2 = models.DecimalField(max_digits=6, decimal_places=2)
    suelo_m2 = models.DecimalField(max_digits=6, decimal_places=2)
    tejado_m2 = models.DecimalField(max_digits=6, decimal_places=2)
    espesores = models.ManyToManyField(Espesor,
                                       related_name='espesores',
                                       blank=True)
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE, related_name="producto")

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    fecha_contacto = models.DateTimeField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    via_entrada = models.CharField(max_length=255, blank=True, null=True)
    comercial = models.ForeignKey(
        Profile,
        on_delete=models.RESTRICT,
        limit_choices_to={'rol': 'comercial'},
        help_text='El rol debe ser "comercial"'
    )

    def __str__(self):
        return f"Cliente: {self.nombre}. Comercial: {self.comercial.user.username}"

class EstadoCliente(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="estados"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="estados"
    )

    fecha_estado = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"El cliente {self.cliente.nombre} está interesado en: {self.producto.nombre}."
