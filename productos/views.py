from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from usuarios.models import Profile, Rol
from .models import Cliente, EstadoCliente, Producto, Espesor
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
    print(Profile)
    print(comerciales)
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

""" para hacer la parte de la lista me he basado en este video https://www.youtube.com/watch?v=vNu3ZsiM2Q8 """
@login_required
def clientes_json(_request):
    clientes = list(Cliente.objects.values())
    data = {'clients': clientes}
    return JsonResponse(data)

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
