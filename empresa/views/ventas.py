# empresa/views/ventas.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from empresa.models import Venta, Producto
from empresa.forms import VentaForm

@login_required
def crear_venta(request):
    empresa = request.user.empresa

    if request.method == 'POST':
        form = VentaForm(request.POST, empresa=empresa)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.empresa = empresa
            venta.save()
            return redirect('listar_ventas')
    else:
        form = VentaForm(empresa=empresa)

    # 📦 Preparamos la lista de productos con id, código, precio y stock
    productos = Producto.objects.filter(empresa=empresa).values(
        'id', 'codigo', 'precio_unitario', 'stock'
    )

    return render(request, 'empresa/crear_venta.html', {
        'form': form,
        'productos_json': list(productos),
    })

@login_required
def listar_ventas(request):
    empresa = request.user.empresa
    ventas = Venta.objects.filter(empresa=empresa).order_by('-fecha')
    return render(request, 'empresa/listar_ventas.html', {'ventas': ventas})
