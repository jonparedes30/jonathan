# empresa/views/cuentas_contables.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from empresa.forms import CuentaContableForm
from empresa.models import CuentaContable

@login_required
def crear_cuenta_contable(request):
    empresa = request.user.empresa

    if request.method == 'POST':
        # Pasamos empresa al form para que lo use en save()
        form = CuentaContableForm(request.POST, empresa=empresa)
        if form.is_valid():
            form.save()  # crea CuentaContable + MovimientoContable
            messages.success(request, '✅ Cuenta contable creada correctamente con su saldo inicial.')
            return redirect('dashboard')
        else:
            messages.error(request, '❌ Corrige los errores en el formulario.')
    else:
        form = CuentaContableForm(empresa=empresa)

    return render(request, 'empresa/crear_cuenta_contable.html', {
        'form': form
    })

@login_required
def listar_cuentas_contables(request):
    empresa = request.user.empresa
    cuentas = CuentaContable.objects.filter(empresa=empresa).order_by('nombre')
    return render(request, 'empresa/listar_cuentas_contables.html', {
        'cuentas': cuentas
    })
