from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.productos, name='productos'),
    path('espesor/<int:espesor_id>/', views.productos, name='productos_espesor'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('producto/<int:producto_id>/', views.edit_producto, name='edit_producto'),
    path('producto/<int:producto_id>/delete/', views.borrar_producto, name='borrar_producto'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/comercial/<int:comercial_id>/', views.clientes, name='clientes_comercial'),
    path('clientes/lista/', views.clientes_lista, name='clientes_lista'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/<int:cliente_id>/delete/', views.borrar_cliente, name='borrar_cliente'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('visitas/', views.visitas, name='visitas'),
    path('acabadas/', views.acabadas, name='acabadas'),
    path('seniales/', views.seniales, name='seniales'),
    path('producto_especifico/<int:producto_especifico_id>/', views.producto_especifico, name='producto_especifico'),
]
