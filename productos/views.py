from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.db.models import Q

from usuarios.models import Profile, Rol
from .models import Cliente, EstadoCliente, Producto, Espesor, ProductoEspecifico, Ubicacion, EstadoProducto, EnvioProducto, EnvioMaterial, ProductoEspesor, TipoProducto
from .forms import ClienteForm, ProductoForm, EnvioProductoForm, EnvioMaterialForm, ProductoEspecificoForm, UbicacionForm, ProductoEspesorForm

@login_required
def productos(request, espesor_id=None):
    espesor = None
    espesores = Espesor.objects.all()
    productos = Producto.objects.all()

    # Filtros de búsqueda
    num_habitaciones = request.GET.get('num_habitaciones')
    num_banios = request.GET.get('num_banios')
    num_plantas = request.GET.get('num_plantas')
    num_cocina = request.GET.get('num_cocina')
    tipo_productos = request.GET.get('tipo_productos')

    if espesor_id:
        espesor = get_object_or_404(Espesor, id_espesor=espesor_id)
        productos = productos.filter(precios_espesor__espesor=espesor).distinct()
    if num_habitaciones:
        productos = productos.filter(num_habitaciones=num_habitaciones)
    if num_banios:
        productos = productos.filter(num_banios=num_banios)
    if num_plantas:
        productos = productos.filter(num_plantas=num_plantas)
    if num_cocina:
        productos = productos.filter(num_cocina=num_cocina)
    if tipo_productos: 
        productos = productos.filter(tipo_productos__slug=tipo_productos).distinct()
    
    tipos = TipoProducto.objects.all()
    habitaciones = productos.values_list('num_habitaciones', flat=True).distinct().order_by('num_habitaciones')
    banios = productos.values_list('num_banios', flat=True).distinct().order_by('num_banios')
    plantas = productos.values_list('num_plantas', flat=True).distinct().order_by('num_plantas')
    cocina = productos.values_list('num_cocina', flat=True).distinct().order_by('num_cocina')

    return render(request, 'products/productos.html', {
        'productos': productos,
        'espesor': espesor,
        'espesores': espesores,
        'tipos': tipos,
        'habitaciones': habitaciones,
        'banios': banios,
        'plantas': plantas,
        'cocina': cocina,
        'filtros': {
            'num_habitaciones': num_habitaciones,
            'num_banios': num_banios,
            'num_plantas': num_plantas,
            'num_cocina': num_cocina,
            'tipo_productos': tipo_productos,
        }
    })

@login_required
def crear_producto(request):
    
    if request.method == 'GET':
        return render(request, "products/crear_producto.html", {
            'form': ProductoForm
        })
    else:
        try:
            form = ProductoForm(request.POST, request.FILES)
            nuevo_producto = form.save(commit=False)
            nuevo_producto.save()
            return redirect('productos:productos')
        except ValueError:
            return render(request, "products/crear_producto.html", {
                'form': ProductoForm,
                'error': 'Por favor, proporciona datos correctos'
            })

@login_required
def edit_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    precios_espesor = producto.precios_espesor.select_related('espesor').all()
    error = None

    if request.method == 'POST':
        # Formulario principal de producto
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        form_espesor = ProductoEspesorForm(request.POST)
        # Verifica si el submit viene del modal de espesores
        if 'espesor' in request.POST and 'precio' in request.POST:
            if form_espesor.is_valid():
                precio_espesor = form_espesor.save(commit=False)
                precio_espesor.producto = producto
                precio_espesor.save()
                return redirect('productos:edit_producto', producto_id=producto.id_producto)
            else:
                error = 'Error al añadir el espesor'
        else:
            if form.is_valid():
                form.save()
                return redirect('productos:productos')
            else:
                error = 'Error al actualizar el producto'
    else:
        form = ProductoForm(instance=producto)
        form_espesor = ProductoEspesorForm()

    return render(request, 'products/edit_producto.html', {
        'producto': producto,
        'form': form,
        'form_espesor': form_espesor,
        'precios_espesor': precios_espesor,
        'error': error,
    })

@login_required
def edit_cliente(request, cliente_id):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
        form = ClienteForm(instance=cliente)
        return render(request, 'clients/edit_cliente.html', {'cliente': cliente, 'form': form})
    else:
        try:
            cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('productos:clientes')
        except  ValueError:
            return render(request, 'clients/edit_cliente.html', {'cliente': cliente, 'form': form, 'error': 'Error al actualizar el cliente'})

@login_required
def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:productos')

@login_required
def clientes(request, estado_slug=None, comercial_id=None):
    estado = None
    comercial = None
    estados = EstadoCliente.objects.all()
    clientes = Cliente.objects.all()

    if estado_slug:
        estado = get_object_or_404(EstadoCliente,
                                   slug=estado_slug)
        clientes = clientes.filter(estado=estado)

    rol = get_object_or_404(Rol,
                            slug='comercial')
    profiles = Profile.objects.filter(user__is_active=True, roles=rol)
    comerciales = profiles
    """ depuración """
    """ print(Profile)
    print(comerciales) """
    if comercial_id:
        comercial = get_object_or_404(Profile,
                                      id=comercial_id,
                                      roles=rol)
        clientes = clientes.filter(comercial=comercial)

    return render(request, 'clients/clientes.html', {'clientes': clientes,
                                                     'estado': estado,
                                                     'estados': estados,
                                                     'comercial': comercial,
                                                     'comerciales': comerciales})

@login_required
def clientes_lista(request, estado_slug=None, comercial_id=None):
    estado = None
    comercial = None
    estados = EstadoCliente.objects.all()
    clientes = Cliente.objects.all()

    if estado_slug:
        estado = get_object_or_404(EstadoCliente,
                                   slug=estado_slug)
        clientes = clientes.filter(estado=estado)

    rol = get_object_or_404(Rol,
                            slug='comercial')
    profiles = Profile.objects.filter(user__is_active=True, roles=rol)
    comerciales = profiles
    """ depuración """
    """ print(Profile)
    print(comerciales) """
    if comercial_id:
        comercial = get_object_or_404(Profile,
                                      id=comercial_id,
                                      roles=rol)
        clientes = clientes.filter(comercial=comercial)

    return render(request, 'clients/clientes_lista.html', {'clientes': clientes,
                                                            'estado': estado,
                                                            'estados': estados,
                                                            'comercial': comercial,
                                                            'comerciales': comerciales})

@login_required
def crear_cliente(request):
    
    if request.method == 'GET':
        return render(request, "clients/crear_cliente.html", {
            'form': ClienteForm
        })
    else:
        try:
            form = ClienteForm(request.POST)
            nuevo_cliente = form.save(commit=False)
            nuevo_cliente.save()
            return redirect('productos:clientes')
        except ValueError:
            return render(request, "clients/crear_cliente.html", {
                'form': ClienteForm,
                'error': 'Por favor, proporciona datos correctos'
            })

@login_required
def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('productos:clientes')

""" 
    Para hacer consultas tipo join en django he visitado este enlace
    https://es.stackoverflow.com/questions/17275/django-como-hacer-consultas-en-varias-tablas-join 
"""
@login_required
def ordenes(request, estado_slug=None):
    estado = None
    estados = EstadoProducto.objects.filter(slug__in=['en-construccion', 'enviado', 'reserva'])
    productos_especificos = ProductoEspecifico.objects.all()
    if estado_slug:
        estado = get_object_or_404(EstadoProducto,
                                   slug=estado_slug)
        productos_especificos = productos_especificos.filter(estado=estado)
    else:
        productos_especificos = productos_especificos.filter(estado__slug__in=['en-construccion', 'enviado', 'reserva'])
    
    return render(request, "prod_esp/ordenes.html", {
        'ordenes': productos_especificos,
        'estado': estado,
        'estados': estados,
    })

@login_required
def visitas(request):
    productos_especificos = ProductoEspecifico.objects.all()
    slug_visita = get_object_or_404(EstadoProducto,
                             slug="visita")
    visitas = productos_especificos.filter(estado=slug_visita)
    return render(request, "prod_esp/visitas.html", {
        'visitas': visitas
    })

@login_required
def acabadas(request):
    productos_especificos = ProductoEspecifico.objects.all()
    slug_acabado = get_object_or_404(EstadoProducto,
                                     slug='acabado')
    acabadas = productos_especificos.filter(estado=slug_acabado)
    return render(request, 'prod_esp/acabadas.html', {
        'acabadas': acabadas
    })

@login_required
def seniales(request, estado_slug=None):
    estado = None
    estados = EstadoProducto.objects.filter(slug__in=['pago-completo', 'pago-parcial'])
    productos_especificos = ProductoEspecifico.objects.all()
    
    if estado_slug:
        estado = get_object_or_404(EstadoProducto,
                                   slug=estado_slug)
        productos_especificos = productos_especificos.filter(estado=estado)
    else:
        productos_especificos = productos_especificos.filter(estado__slug__in=['pago-completo', 'pago-parcial'])
    
    return render(request, 'prod_esp/seniales.html', {
        'seniales': productos_especificos,
        'estado': estado,
        'estados': estados,
    })

@login_required
def producto_especifico(request, producto_especifico_id):
    prod_esp = get_object_or_404(ProductoEspecifico,
                                id_prod_espe=producto_especifico_id)
    
    ubi = Ubicacion.objects.filter(producto_especifico=prod_esp)

    envio_producto = EnvioProducto.objects.filter(producto_especifico=prod_esp)
    envio_material = EnvioMaterial.objects.filter(producto_especifico=prod_esp)
    
    if request.method == "POST":
        if 'producto' in request.POST:
            form_envio_producto = EnvioProductoForm(request.POST)
            if form_envio_producto.is_valid():
                envio = form_envio_producto.save(commit=False)
                envio.producto_especifico = prod_esp
                envio.save()
                return redirect('productos:producto_especifico', producto_especifico_id=prod_esp.id_prod_espe)
        elif 'material' in request.POST:
            form_envio_material = EnvioMaterialForm(request.POST)
            if form_envio_material.is_valid():
                envio = form_envio_material.save(commit=False)
                envio.producto_especifico = prod_esp
                envio.save()
                return redirect('productos:producto_especifico', producto_especifico_id=prod_esp.id_prod_espe)
    else:
        form_envio_producto = EnvioProductoForm()
        form_envio_material = EnvioMaterialForm()

    return render(request, 'prod_esp/producto_especifico.html', {
        'prod_esp': prod_esp,
        'ubi': ubi,
        'envio_producto': envio_producto,
        'envio_material': envio_material,
        'form_envio_producto': EnvioProductoForm,
        'form_envio_material': EnvioMaterialForm,
    })

@login_required
def aniadir_producto_especifico(request):
    if request.method == 'GET':
        return render(request, "prod_esp/aniadir_producto_especifico.html", {
            'form_prod_esp': ProductoEspecificoForm,
            'form_ubicacion': UbicacionForm,
        })
    else:
        try:
            form = ProductoEspecificoForm(request.POST)
            nuevo_producto_especifico = form.save(commit=False)
            nuevo_producto_especifico.save()
            return redirect('home:home')
        except ValueError:
            return render(request, "prod_esp/aniadir_producto_especifico.html", {
                'form_prod_esp': ProductoEspecificoForm,
                'form_ubicacion': UbicacionForm,
                'error': 'Por favor, proporciona datos correctos'
            })

@login_required
def editar_producto_especifico(request, producto_especifico_id):
    if request.method == 'GET':
        prod_esp = get_object_or_404(ProductoEspecifico, id_prod_espe=producto_especifico_id)
        form_prod_esp = ProductoEspecificoForm(instance=prod_esp)
        form_ubicacion = UbicacionForm()
        return render(request, 'prod_esp/editar_producto_especifico.html', {
            'prod_esp': prod_esp, 
            'form_prod_esp': form_prod_esp,
            'form_ubicacion': form_ubicacion
            })
    else:
        try:
            prod_esp = get_object_or_404(ProductoEspecifico, id_prod_espe=producto_especifico_id)
            form_prod_esp = ProductoEspecificoForm(data=request.POST, instance=prod_esp)
            form_ubicacion = UbicacionForm(data=request.POST)
            form_prod_esp.save()
            return redirect('home:home')
        except ValueError:
            return render(request, 'prod_esp/editar_producto_especifico.html', {
                'prod_esp': prod_esp,
                'form_prod_esp': form_prod_esp,
                'form_ubicacion': form_ubicacion,
                'error': 'Error al actualizar el producto específico'})

@login_required
def borrar_producto_especifico(request, producto_especifico_id):
    prod_esp = get_object_or_404(ProductoEspecifico, pk=producto_especifico_id)
    if request.method == 'POST':
        prod_esp.delete()
        return redirect('home:home')

@login_required
def borrar_envio_producto_especifico(request, id_envio):
    envio_producto_esp = get_object_or_404(EnvioProducto, id_envio=id_envio)
    if request.method == 'POST':
        envio_producto_esp.delete()
        return redirect('productos:producto_especifico', producto_especifico_id=envio_producto_esp.producto_especifico.id_prod_espe)

@login_required
def borrar_envio_material_especifico(request, id_envio):
    envio_material_esp = get_object_or_404(EnvioMaterial, id_envio=id_envio)
    if request.method == 'POST':
        envio_material_esp.delete()
        return redirect('productos:producto_especifico', producto_especifico_id=envio_material_esp.producto_especifico.id_prod_espe)