from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from empresa.models import Venta, Compra, Gasto, CuentaContable, MovimientoContable

# ======================
# ESTADO DE RESULTADOS
# ======================
@login_required
def estado_resultados(request):
    empresa = request.user.empresa

    total_ventas = Venta.objects.filter(empresa=empresa).aggregate(total=Sum('monto'))['total'] or 0

    compras = Compra.objects.filter(empresa=empresa)
    total_costos = sum(c.precio_unitario * c.cantidad for c in compras)

    total_gastos = Gasto.objects.filter(empresa=empresa).aggregate(total=Sum('monto'))['total'] or 0

    utilidad_operativa = total_ventas - total_costos
    utilidad_neta = utilidad_operativa - total_gastos

    return render(request, 'empresa/estado_resultado.html', {
        'ventas': total_ventas,
        'costos': total_costos,
        'gastos': total_gastos,
        'utilidad_operativa': utilidad_operativa,
        'utilidad_neta': utilidad_neta,
    })

# ======================
# FLUJO DE CAJA ESTIMADO
# ======================
@login_required
def flujo_caja(request):
    empresa    = request.user.empresa
    hoy        = datetime.today()
    año_actual = hoy.year
    meses      = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

    flujo = []
    for idx, mes_nombre in enumerate(meses, start=1):
        ventas_mes = (
            Venta.objects.filter(
                empresa=empresa,
                fecha__year=año_actual,
                fecha__month=idx
            )
            .aggregate(total_sum=Sum('total'))['total_sum'] or 0
        )
        compras_mes = (
            Compra.objects.filter(
                empresa=empresa,
                fecha__year=año_actual,
                fecha__month=idx
            )
            .aggregate(total_sum=Sum('total'))['total_sum'] or 0
        )
        gastos_mes = (
            Gasto.objects.filter(
                empresa=empresa,
                fecha__year=año_actual,
                fecha__month=idx
            )
            .aggregate(monto_sum=Sum('monto'))['monto_sum'] or 0
        )
        entrada = ventas_mes
        salida  = compras_mes + gastos_mes
        neto    = entrada - salida

        flujo.append({
            'mes':     mes_nombre,
            'entrada': entrada,
            'salida':  salida,
            'neto':    neto,
        })

    return render(request, 'empresa/flujo_caja.html', {
        'flujo':  flujo,
        'labels': meses,
    })

@login_required
def balance_general(request):
    empresa = request.user.empresa

    # 1) Activos agrupados por cuenta
    activos_qs = (
        MovimientoContable.objects
        .filter(empresa=empresa, cuenta_fk__tipo='activo')
        .values('cuenta_fk__nombre')
        .annotate(valor=Sum('monto'))
    )

    # 2) Pasivos agrupados por cuenta
    pasivos_qs = (
        MovimientoContable.objects
        .filter(empresa=empresa, cuenta_fk__tipo='pasivo')
        .values('cuenta_fk__nombre')
        .annotate(valor=Sum('monto'))
    )

    # 3) Totales
    total_activos    = sum(item['valor'] for item in activos_qs) or 0
    total_pasivos    = sum(item['valor'] for item in pasivos_qs) or 0
    total_patrimonio = total_activos - total_pasivos

    contexto = {
        'activos': activos_qs,
        'pasivos': pasivos_qs,
        'total_activos': total_activos,
        'total_pasivos': total_pasivos,
        'total_patrimonio': total_patrimonio,
    }
    return render(request, 'empresa/balance_general.html', contexto)

# ======================
# REGISTRO DE MOVIMIENTOS
# ======================
def registrar_movimiento_contable(empresa, cuenta_nombre, monto, descripcion, tipo='debito', tipo_cuenta='activo'):
    cuenta, _ = CuentaContable.objects.get_or_create(
        empresa=empresa,
        nombre__icontains=cuenta_nombre,
        defaults={'nombre': cuenta_nombre, 'tipo': tipo_cuenta}
    )

    MovimientoContable.objects.create(
        empresa=empresa,
        cuenta=cuenta,
        tipo=tipo,
        monto=monto,
        descripcion=descripcion
    )
