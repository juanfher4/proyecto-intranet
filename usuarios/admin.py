from django.contrib import admin
from .models import Rol, Profile

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'fecha_nacimiento', 'display_roles']
    raw_id_fields = ['user']
    list_filter = ['roles']
    filter_horizontal = ['roles']

    def display_roles(self, obj):
        lista_roles = []
        for rol in obj.roles.all():
            lista_roles.append(rol.nombre)
        return ", ".join(lista_roles)
    display_roles.short_description = 'Roles'
