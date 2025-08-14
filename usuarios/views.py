from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserEditForm, ProfileEditForm
from .models import Profile, Rol


@login_required
def signout(request):
    logout(request)
    return redirect('usuarios:login')

"""
def signin(request):

    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {
            'form': form
        })
    else:
        form = AuthenticationForm
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'El usuario o la contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('home:home') """

@login_required
def profile_detail(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        profile = request.user.profile
        messages.info(request, "Se ha creado automáticamente tu perfil")
    return render(request, 'account/perfil_detail.html', {
        'user': request.user,
        'profile': profile
    })

@login_required
def edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "Se ha creado automáticamente tu perfil")
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })

@login_required
def profile_list(request, rol_slug=None):
    profile, created = Profile.objects.get_or_create(user=request.user)
    rol = None
    roles = Rol.objects.all()
    profiles = Profile.objects.filter(user__is_active=True)

    if rol_slug:
        rol = get_object_or_404(Rol,
                                slug=rol_slug)
        profiles = profiles.filter(roles=rol)

    return render(request,
                  'profiles/list.html',
                  {'rol': rol,
                   'roles': roles,
                   'profiles': profiles,
                   'profile': profile})
