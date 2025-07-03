from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from empresa.models import Venta, Gasto
import calendar
from datetime import datetime

@login_required
def dashboard(request):
    empresa = request.user.empresa

    total_ventas = Venta.objects.filter(empresa=empresa).aggregate(total=Sum('total'))['total'] or 0
    total_gastos = Gasto.objects.filter(empresa=empresa).aggregate(total=Sum('monto'))['total'] or 0
    utilidad_neta = total_ventas - total_gastos
    rentabilidad = (utilidad_neta / total_ventas * 100) if total_ventas > 0 else 0

    # Gráfico: últimos 12 meses hasta el mes actual
    hoy = datetime.today()
    ventas_mensuales = []
    gastos_mensuales = []
    labels_meses = []

    for i in range(12):
        mes = (hoy.month - i - 1) % 12 + 1
        anio = hoy.year if hoy.month - i > 0 else hoy.year - 1
        nombre_mes = calendar.month_abbr[mes]

        labels_meses.insert(0, nombre_mes)
        ventas_mes = Venta.objects.filter(
            empresa=empresa,
            fecha__month=mes,
            fecha__year=anio
        ).aggregate(total=Sum('total'))['total'] or 0

        gastos_mes = Gasto.objects.filter(
            empresa=empresa,
            fecha__month=mes,
            fecha__year=anio
        ).aggregate(total=Sum('monto'))['total'] or 0

        ventas_mensuales.insert(0, float(ventas_mes))
        gastos_mensuales.insert(0, float(gastos_mes))

    contexto = {
        'total_ventas': round(total_ventas, 2),
        'total_gastos': round(total_gastos, 2),
        'utilidad_neta': round(utilidad_neta, 2),
        'rentabilidad': round(rentabilidad, 2),
        'labels_meses': labels_meses,
        'ventas_mensuales': ventas_mensuales,
        'gastos_mensuales': gastos_mensuales
    }

    return render(request, 'empresa/dashboard.html', contexto)
