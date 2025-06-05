from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.db.models import Q

from usuarios.models import Profile, Rol
from .models import Cliente, EstadoCliente, Producto, Espesor, ProductoEspecifico, Ubicacion, EstadoProducto, EnvioProducto, EnvioMaterial
from .forms import ClienteForm, ProductoForm

@login_required
def productos(request, espesor_id=None):
    espesor = None
    espesores = Espesor.objects.all()
    productos = Producto.objects.all()

    if espesor_id:
        espesor = get_object_or_404(Espesor,
                                    id_espesor=espesor_id)
        productos = productos.filter(espesores=espesor)

    return render(request, 'products/productos.html', {'productos': productos,
                                                       'espesor': espesor,
                                                       'espesores': espesores})

@login_required
def crear_producto(request):
    
    if request.method == 'GET':
        return render(request, "products/crear_producto.html", {
            'form': ProductoForm
        })
    else:
        try:
            form = ProductoForm(request.POST)
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
    if request.method == 'GET':
        producto = get_object_or_404(Producto, id_producto=producto_id)
        form = ProductoForm(instance=producto)
        return render(request, 'products/edit_producto.html', {'producto': producto, 'form': form})
    else:
        try:
            producto = get_object_or_404(Producto, id_producto=producto_id)
            form = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
            form.save()
            return redirect('productos:productos')
        except ValueError:
            return render(request, 'products/edit_producto.html', {'producto': producto, 'form': form, 'error': 'Error al actualizar el producto'})

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
        clientes = clientes.filter(estados=estado)

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
def clientes_lista(request, estado_slug=None):
    estado = None
    estados = EstadoCliente.objects.all()
    clientes = Cliente.objects.all()

    if estado_slug:
        estado = get_object_or_404(EstadoCliente,
                                   slug=estado_slug)
        clientes = clientes.filter(estados=estado)

    return render(request, 'clients/clientes_lista.html', {'clientes': clientes,
                                                     'estado': estado,
                                                     'estados': estados})


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
def ordenes(request):
    productos_especificos = ProductoEspecifico.objects.all()
    slug_en_construccion = get_object_or_404(EstadoProducto,
                                     slug='en-construccion')
    slug_enviado = get_object_or_404(EstadoProducto,
                                     slug='enviado')
    slug_reserva = get_object_or_404(EstadoProducto,
                                     slug='reserva')
    ordenes = productos_especificos.filter(Q(estado=slug_en_construccion) | Q(estado=slug_enviado) | Q(estado=slug_reserva))
    return render(request, "prod_esp/ordenes.html", {
        'ordenes': ordenes
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
def seniales(request):
    productos_especificos = ProductoEspecifico.objects.all()
    slug_pago_completo = get_object_or_404(EstadoProducto,
                                     slug='pago-completo')
    slug_pago_parcial = get_object_or_404(EstadoProducto,
                                     slug='pago-parcial')
    seniales = productos_especificos.filter(Q(estado=slug_pago_completo) | Q(estado=slug_pago_parcial))
    return render(request, 'prod_esp/seniales.html', {
        'seniales': seniales
    })

@login_required
def producto_especifico(request, producto_especifico_id):
    prod_esp = get_object_or_404(ProductoEspecifico,
                                id_prod_espe=producto_especifico_id)
    ubi = Ubicacion.objects.filter(producto_especifico=prod_esp)
    envio_producto = EnvioProducto.objects.filter(producto_especifico=prod_esp)
    envio_material = EnvioMaterial.objects.filter(producto_especifico=prod_esp)
    return render(request, 'prod_esp/producto_especifico.html', {
        'prod_esp': prod_esp,
        'ubi': ubi,
        'envio_producto': envio_producto,
        'envio_material': envio_material
    })
