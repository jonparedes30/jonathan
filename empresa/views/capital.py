from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from empresa.forms import CapitalForm
from empresa.models import MovimientoContable, CuentaContable
from empresa.views.contabilidad import registrar_movimiento_contable


@login_required
def crear_capital(request):
    if request.method == 'POST':
        monto = float(request.POST.get('monto'))
        descripcion = request.POST.get('descripcion')
        empresa = request.user.empresa

        if not empresa:
            return HttpResponse("No se encontró empresa para este usuario", status=400)

        # Crear o recuperar cuenta contable
        cuenta, _ = CuentaContable.objects.get_or_create(
            empresa=empresa,
            nombre='Capital Social',
            defaults={'tipo': 'patrimonio'}
        )

        # Registrar el movimiento contable
        registrar_movimiento_contable(
            empresa=empresa,
            cuenta_nombre='Capital Social',
            monto=monto,
            descripcion=descripcion,
            tipo='credito',
            tipo_cuenta='patrimonio'
        )

        return redirect('resumen_financiero')

    return render(request, 'empresa/registrar_capital.html')


@login_required
def listar_capital(request):
    empresa = request.user.empresa
    movimientos = MovimientoContable.objects.filter(
        empresa=empresa,
        cuenta__tipo='patrimonio'
    ).order_by('-fecha')

    return render(request, 'empresa/listar_capital.html', {'movimientos': movimientos})
