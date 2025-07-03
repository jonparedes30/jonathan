from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from empresa.models import Meta  # ← Ya que ahora está en models.py
from datetime import datetime

@login_required
def gestionar_metas(request):
    empresa = request.user.empresa

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        objetivo_mensual = request.POST.get('objetivo_mensual')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')

        if tipo and objetivo_mensual and mes and anio:
            Meta.objects.create(
                empresa=empresa,
                tipo=tipo,
                objetivo_mensual=objetivo_mensual,
                mes=int(mes),
                anio=int(anio)
            )
            return redirect('gestionar_metas')

    metas = Meta.objects.filter(empresa=empresa).order_by('-creado_en')
    return render(request, 'empresa/metas.html', {'metas': metas})
