from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from empresa.models import Empresa
from empresa.forms import EmpresaForm


@login_required
def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'empresa/crear_empresa.html', {'form': form})


@login_required
def listar_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'empresa/listar_empresas.html', {'empresas': empresas})
