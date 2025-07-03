# empresa/views/resumen.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from empresa.models import Venta, Compra, Gasto
from django.db.models import Sum
from datetime import datetime

@login_required
def resumen_financiero(request):
    empresa = request.user.empresa
    ventas = Venta.objects.filter(empresa=empresa).aggregate(total=Sum('total'))['total'] or 0
    compras = Compra.objects.filter(empresa=empresa).aggregate(total=Sum('total'))['total'] or 0
    gastos = Gasto.objects.filter(empresa=empresa).aggregate(total=Sum('monto'))['total'] or 0

    utilidad_bruta = ventas - compras
    utilidad_neta = utilidad_bruta - gastos

    contexto = {
        'ventas': ventas,
        'compras': compras,
        'gastos': gastos,
        'utilidad_bruta': utilidad_bruta,
        'utilidad_neta': utilidad_neta,
    }
    return render(request, 'empresa/resumen_financiero.html', contexto)

@login_required
def estado_resultados(request):
    empresa = request.user.empresa

    # Ventas y Compras usan el campo 'total'
    ventas  = Venta.objects.filter(empresa=empresa) \
              .aggregate(total_sum=Sum('total'))['total_sum'] or 0
    compras = Compra.objects.filter(empresa=empresa) \
              .aggregate(total_sum=Sum('total'))['total_sum'] or 0

    # Gastos usa el campo 'monto'
    gastos  = Gasto.objects.filter(empresa=empresa) \
              .aggregate(monto_sum=Sum('monto'))['monto_sum'] or 0

    utilidad_operativa = ventas - compras
    utilidad_neta      = utilidad_operativa - gastos

    contexto = {
        'ventas':             ventas,
        'compras':            compras,
        'gastos':             gastos,
        'utilidad_operativa': utilidad_operativa,
        'utilidad_neta':      utilidad_neta,
    }
    return render(request, 'empresa/estado_resultado.html', contexto)
