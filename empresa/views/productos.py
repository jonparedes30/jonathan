from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from empresa.models import Producto
from empresa.forms import ProductoForm


@login_required
def crear_producto(request):
    empresa = request.user.empresa

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.empresa = empresa
            producto.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()

    return render(request, 'empresa/crear_producto.html', {'form': form})


@login_required
def listar_productos(request):
    empresa = request.user.empresa
    productos = Producto.objects.filter(empresa=empresa).order_by('nombre')
    return render(request, 'empresa/listar_productos.html', {'productos': productos})


@login_required
def obtener_info_producto(request):
    codigo = request.GET.get('codigo', '')
    producto = Producto.objects.filter(codigo=codigo).first()

    if producto:
        data = {
            'nombre': producto.nombre,
            'precio': float(producto.precio_unitario),
            'stock': producto.stock,
        }
    else:
        data = {'error': 'Producto no encontrado'}

    return JsonResponse(data)
