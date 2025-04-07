from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes'),
]
