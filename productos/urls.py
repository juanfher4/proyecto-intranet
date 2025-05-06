from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.productos, name='productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('<int:producto_id>/', views.edit_producto, name='edit_producto'),
    path('<int:producto_id>/delete/', views.borrar_producto, name='borrar_producto'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:comercial_id>/', views.clientes, name='clientes_comercial'),
    path('clientes/lista/', views.clientes_lista, name='clientes_lista'),
    path('clientes/json/', views.clientes_json, name='clientes_json'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/<int:cliente_id>/delete/', views.borrar_cliente, name='borrar_cliente'),
]
