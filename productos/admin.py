from django.contrib import admin
from .models import Cliente, EstadoCliente, Producto, Espesor, Ubicacion, EstadoProducto, ProductoEspecifico, TipoProducto, Montador, Material, Proveedor, EnvioMaterial, EnvioProducto

@admin.register(EstadoCliente)
class EstadoClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'fecha_contacto', 'via_entrada', 'comercial', 'estado']

@admin.register(Espesor)
class EspesorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'revestimiento']
    list_filter = ['revestimiento']

@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'display_espesores', 'display_tipos']
    list_filter = ['tipo_productos', 'espesores', 'num_habitaciones', 'num_plantas', 'num_banios', 'precio']

    def display_tipos(self, obj):
        lista_tipos = []
        for tipo in obj.tipo_productos.all():
            lista_tipos.append(tipo.nombre)
        return ", ".join(lista_tipos)
    display_tipos.short_description = 'Tipos'    

    def display_espesores(self, obj):
        lista_espesores = []
        for espesor in obj.espesores.all():
            if espesor.revestimiento:
                revestimiento = "rev"
                lista_espesores.append(f"{espesor.nombre} ({revestimiento})")
            else:
                revestimiento = ""
                lista_espesores.append(f"{espesor.nombre}")
        return ", ".join(lista_espesores)
    display_espesores.short_description = 'Espesores'

@admin.register(EstadoProducto)
class EstadoProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}

class UbicacionInline(admin.StackedInline):
    model = Ubicacion
    extra = 1
    fields = ['latitud', 'longitud']

@admin.register(ProductoEspecifico)
class ProductoEspecificoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'montador', 'fecha_inicio_montaje', 'fecha_acabado_montaje']
    list_filter = ['montador']
    search_fields = ['producto__nombre', 'cliente__nombre']
    inlines = [UbicacionInline]

@admin.register(Montador)
class MontadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'zona_servicio']
    list_filter = ['zona_servicio']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'nota']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'display_proveedores']
    prepopulated_fields = {'slug': ('nombre',)}

    def display_proveedores(self, obj):
        lista_proveedores = []
        for proveedor in obj.proveedores.all():
            lista_proveedores.append(proveedor.nombre)
        return ", ".join(lista_proveedores)
    display_proveedores.short_description = 'Proveedores'

@admin.register(EnvioProducto)
class EnvioProductoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'proveedor', 'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real', 'estado']

@admin.register(EnvioMaterial)
class EnvioMaterialAdmin(admin.ModelAdmin):
    list_display = ['material', 'proveedor', 'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real', 'estado']
