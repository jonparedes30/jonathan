# empresa/views/compras.py

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from empresa.models import Compra, Producto
from empresa.forms import CompraForm

@login_required
def crear_compra(request):
    empresa = request.user.empresa

    if request.method == 'POST':
        form = CompraForm(request.POST, empresa=empresa)
        if form.is_valid():
            form.save()
            return redirect('listar_compras')
    else:
        form = CompraForm(empresa=empresa)

    # Preparar JSON de productos para el JS
    productos = Producto.objects.filter(empresa=empresa).values(
        'id', 'codigo', 'precio_unitario', 'stock'
    )
    productos_json = json.dumps(list(productos))

    return render(request, 'empresa/crear_compra.html', {
        'form': form,
        'productos_json': productos_json,
    })


@login_required
def listar_compras(request):
    empresa = request.user.empresa
    compras = Compra.objects.filter(empresa=empresa).order_by('-fecha')
    return render(request, 'empresa/listar_compras.html', {
        'compras': compras,
    })
