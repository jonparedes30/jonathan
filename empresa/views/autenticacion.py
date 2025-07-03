# empresa/views/autenticacion.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from empresa.forms import RegistroForm  # Importación corregida

def login_usuario(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('resumen_financiero')
        messages.error(request, 'Credenciales inválidas')
    return render(request, 'empresa/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('login')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta y empresa creadas exitosamente.')
            return redirect('login')
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()
    return render(request, 'empresa/registro.html', {
        'form': form,
    })
