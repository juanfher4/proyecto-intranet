from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .forms import TaskForm
from .models import Task
from productos.models import ProductoEspecifico, EnvioProducto, EnvioMaterial, EstadoProducto

""" 
Video de consultas con filtros
https://www.youtube.com/watch?v=yzw7kepT7y0
"""

@login_required
def home(request):
    productos_especificos = ProductoEspecifico.objects.all()

    """ Para el div de órdenes """
    slug_en_construccion = get_object_or_404(EstadoProducto,
                                     slug='en-construccion')
    slug_enviado = get_object_or_404(EstadoProducto,
                                     slug='enviado')
    slug_reserva = get_object_or_404(EstadoProducto,
                                     slug='reserva')
    ordenes = productos_especificos.filter(Q(estado=slug_en_construccion) | Q(estado=slug_enviado) | Q(estado=slug_reserva))[:5]

    """ Para el div de vivitas """
    
    slug_visita = get_object_or_404(EstadoProducto,
                             slug="visita")
    visitas = productos_especificos.filter(estado=slug_visita)

    """ Para el div de acabadas """

    slug_acabado = get_object_or_404(EstadoProducto,
                                     slug='acabado')
    acabadas = productos_especificos.filter(estado=slug_acabado)

    """ Para el div de señales """
    
    slug_pago_completo = get_object_or_404(EstadoProducto,
                                     slug='pago-completo')
    slug_pago_parcial = get_object_or_404(EstadoProducto,
                                     slug='pago-parcial')
    seniales = productos_especificos.filter(Q(estado=slug_pago_completo) | Q(estado=slug_pago_parcial))

    return render(request, 'home.html', {
        'ordenes': ordenes,
        'visitas': visitas,
        'acabadas': acabadas,
        'seniales': seniales
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, "create_task.html", {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home:tasks')
        except ValueError:
            return render(request, "create_task.html", {
                'form': TaskForm,
                'error': 'Por favor, proporciona datos correctos'
            })
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('home:tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error al actualizar la tarea'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('home:tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('home:tasks')
