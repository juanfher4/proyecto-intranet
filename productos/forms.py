from django import forms
from .models import Cliente, Producto, ProductoEspesor, TipoProducto, ProductoEspecifico, Ubicacion, EnvioProducto, EnvioMaterial, Material, Proveedor

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'ciudad', 'fecha_contacto', 'nota', 'via_entrada', 'comercial', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe el correo'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe la ciudad'}),
            'fecha_contacto': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'nota': forms.Textarea(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe una nota'}),
            'via_entrada': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe la via de entrada'}),
            'comercial': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'estado': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
        }
        labels = {
            'fecha_contacto': 'Fecha de contacto',
            'via_entrada': 'Vía de entrada',
        }

class ProductoForm(forms.ModelForm):
    tipo_productos = forms.ModelMultipleChoiceField(
        queryset = TipoProducto.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    class Meta:
        model = Producto
        fields = ['nombre', 'num_habitaciones', 'num_banios', 'num_cocina', 'num_plantas', 'pared_m2', 'suelo_m2', 'tejado_m2', 'tipo_productos', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Nombre'}),
            'num_habitaciones': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Número de habitaciones'}),
            'num_banios': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Número de baños'}),
            'num_cocina': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Número de cocinas'}),
            'num_plantas': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Número de plantas'}),
            'pared_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'pared_m2'}),
            'suelo_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'suelo_m2'}),
            'tejado_m2': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'tejado_m2'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control p-2 m-1'}),
        }
        labels = {
            'num_habitaciones': 'Número de habitaciones',
            'num_banios': 'Número de baños',
            'num_plantas': 'Número de plantas',
            'tipo_productos': 'Tipo de producto',
        }

class ProductoEspesorForm(forms.ModelForm):
    class Meta:
        model = ProductoEspesor
        fields = ['espesor', 'precio']
        widgets = {
            'espesor': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
        }

class ProductoEspecificoForm(forms.ModelForm):
    class Meta:
        model = ProductoEspecifico
        fields = ['producto', 'cliente', 'montador', 'precio', 'fecha_inicio_montaje', 'fecha_acabado_montaje_estimado', 'fecha_acabado_montaje', 'estado']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'cliente': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'montador': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Precio'}),
            'fecha_inicio_montaje': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_acabado_montaje_estimado': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_acabado_montaje': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
        }

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['latitud', 'longitud']
        widgets = {
            'latitud': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Latitud'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Longitud'}),
        }

class EnvioProductoForm(forms.ModelForm):
    class Meta:
        model = EnvioProducto
        fields = ['producto', 'proveedor', 'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real', 'estado', 'cantidad', 'nota', 'producto_especifico']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'proveedor': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_llegada_real': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Cantidad'}),
            'nota': forms.Textarea(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe una nota'}),
            'producto_especifico': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
        }
    
class EnvioMaterialForm(forms.ModelForm):
    class Meta:
        model = EnvioMaterial
        fields = ['material', 'proveedor', 'fecha_salida', 'fecha_llegada_estimada', 'fecha_llegada_real', 'estado', 'cantidad', 'nota', 'producto_especifico']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'proveedor': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'fecha_llegada_real': forms.DateTimeInput(attrs={'class': 'form-control p-2 m-1', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Cantidad'}),
            'nota': forms.Textarea(attrs={'class': 'form-control p-2 m-1', 'placeholder': 'Escribe una nota'}),
            'producto_especifico': forms.Select(attrs={'class': 'form-control p-2 m-1'}),
        }
