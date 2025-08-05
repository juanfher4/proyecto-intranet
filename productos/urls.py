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
    path('clientes/estado/<slug:estado_slug>/', views.clientes, name='clientes_estado'),
    path('clientes/lista/', views.clientes_lista, name='clientes_lista'),
    path('clientes/lista/comercial/<int:comercial_id>/', views.clientes_lista, name='clientes_lista_comercial'),
    path('clientes/lista/estado/<slug:estado_slug>/', views.clientes_lista, name='clientes_lista_estado'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/<int:cliente_id>/delete/', views.borrar_cliente, name='borrar_cliente'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes/estado/<slug:estado_slug>/', views.ordenes, name='ordenes_estado'),
    path('visitas/', views.visitas, name='visitas'),
    path('acabadas/', views.acabadas, name='acabadas'),
    path('seniales/', views.seniales, name='seniales'),
    path('seniales/estado/<slug:estado_slug>/', views.seniales, name='seniales_estado'),
    path('producto_especifico/<int:producto_especifico_id>/', views.producto_especifico, name='producto_especifico'),
    path('producto_especifico/aniadir/', views.aniadir_producto_especifico, name='aniadir_producto_especifico'),
    path('producto_especifico/editar/<int:producto_especifico_id>/', views.editar_producto_especifico, name='editar_producto_especifico'),
    path('producto_especifico/borrar/<int:producto_especifico_id>/', views.borrar_producto_especifico, name='borrar_producto_especifico'),
    path('producto_especifico/borrar_envio_prod_esp/<int:id_envio>/', views.borrar_envio_producto_especifico, name='borrar_envio_producto_especifico'),
    path('producto_especifico/borrar_envio_mat_esp/<int:id_envio>/', views.borrar_envio_material_especifico, name='borrar_envio_material_especifico'),
]
