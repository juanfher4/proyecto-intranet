from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('<slug:rol_slug>', views.profile_list, name='profile_list_rol'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.signout, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('perfil/', views.profile_detail, name='perfil'),
    path('perfil/edit/', views.edit, name='edit'),
]
