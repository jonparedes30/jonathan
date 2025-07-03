from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from empresa.models import Gasto
from empresa.forms import GastoForm
from django.db.models import Sum

@login_required
def crear_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.empresa = request.user.empresa
            gasto.save()
            return redirect('listar_gastos')
    else:
        form = GastoForm()
    return render(request, 'empresa/crear_gasto.html', {'form': form})

@login_required
def listar_gastos(request):
    gastos = Gasto.objects.filter(empresa=request.user.empresa)
    total = gastos.aggregate(Sum('monto'))['monto__sum'] or 0
    return render(request, 'empresa/listar_gastos.html', {
        'gastos': gastos,
        'total': total
    })
