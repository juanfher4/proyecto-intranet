from django.db import models
from usuarios.models import Profile
from django.urls import reverse

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255, blank=True, null=True)
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

class Espesor(models.Model):
    id_espesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    revestimiento = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - Rev: {self.revestimiento}"
    
    def get_absolute_url(self):
        return reverse('usuarios:profile_list_rol',
                       args=[self.id_espesor])

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    class Meta:
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre'])
        ]

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('productos:producto_tipo',
                       args=[self.slug])

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    num_habitaciones = models.IntegerField(blank=True, null=True)
    num_banios = models.IntegerField(blank=True, null=True)
    num_plantas = models.IntegerField(blank=True, null=True)
    num_cocina = models.IntegerField(blank=True, null=True)
    pared_m2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    suelo_m2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tejado_m2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    espesores = models.ManyToManyField(Espesor,
                                       related_name='productos',
                                       blank=True)
    tipo_productos = models.ManyToManyField(TipoProducto,
                                            related_name='productos')
    imagen = models.ImageField(upload_to='products/%Y/%m/%d',
                               blank=True)

    def __str__(self):
        return f"{self.nombre}"

class EstadoCliente(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.nombre

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
        limit_choices_to={'roles__slug': 'comercial'},
        help_text='El rol debe ser "comercial"'
    )
    estado = models.ForeignKey(
        EstadoCliente,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table='cliente'

    def __str__(self):
        return f"Cliente: {self.nombre}. Comercial: {self.comercial.user.username}"

class Montador(models.Model):
    id_montador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    zona_servicio = models.CharField(max_length=255)
    nota = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Montador: {self.nombre}"

class EstadoProducto(models.Model):
    id_estado_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class ProductoEspecifico(models.Model):
    id_prod_espe = models.AutoField(primary_key=True)
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,
        related_name="producto_especifico"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="producto_especifico"
    )
    montador = models.ForeignKey(
        Montador,
        on_delete=models.CASCADE,
        related_name="producto_especifico"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_inicio_montaje = models.DateTimeField()
    fecha_acabado_montaje_estimado = models.DateTimeField(blank=True, null=True)
    fecha_acabado_montaje = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey(
        EstadoProducto,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Producto de {self.cliente.nombre} montado por {self.montador.nombre}"

class Ubicacion(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    producto_especifico = models.ForeignKey(
        ProductoEspecifico,
        on_delete=models.CASCADE,
        related_name='ubicaciones',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Ubicación ({self.latitud}, {self.longitud})"

class EnvioProducto(models.Model):
    id_envio = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="envios_producto"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name="envios_producto"
    )
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField(blank=True, null=True)
    fecha_llegada_real = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=[
            ("listo_envio", "Listo para envío"),
            ("fabricando", "Fabricando"),
            ("pendiente_planos", "Pendiente de confirmar los planos"),
        ],
        default="pendiente_planos"
    )
    cantidad = models.IntegerField(default=1)
    nota = models.TextField(blank=True, null=True)
    producto_especifico = models.ForeignKey(
        ProductoEspecifico,
        on_delete=models.CASCADE,
        related_name='envios_producto',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Envío de {self.producto.nombre} de {self.proveedor.nombre}."

class EnvioMaterial(models.Model):
    id_envio = models.AutoField(primary_key=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="envios_material"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name="envios_material"
    )
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField(blank=True, null=True)
    fecha_llegada_real = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=[
            ("listo_envio", "Listo para envío"),
            ("fabricando", "Fabricando"),
            ("pendiente_planos", "Pendiente de confirmar los planos"),
        ],
        default="pendiente_planos"
    )
    cantidad = models.IntegerField(default=1)
    nota = models.TextField(blank=True, null=True)
    producto_especifico = models.ForeignKey(
        ProductoEspecifico,
        on_delete=models.CASCADE,
        related_name='envios_material',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Envío de {self.material.nombre} de {self.proveedor.nombre}."
