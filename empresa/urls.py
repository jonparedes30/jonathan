from django.urls import path

# Productos
from empresa.views.productos import (
    crear_producto,
    listar_productos,
    obtener_info_producto,
)

# Ventas
from empresa.views.ventas import (
    crear_venta,
    listar_ventas,
)

# Compras
from empresa.views.compras import (
    crear_compra,
    listar_compras,
)

# Gastos
from empresa.views.gastos import (
    crear_gasto,
    listar_gastos,
)

# Capital
from empresa.views.capital import (
    crear_capital,
    listar_capital,
)

# Cuentas contables
from empresa.views.cuentas_contables import (
    crear_cuenta_contable,
    listar_cuentas_contables,
)

# Empresa y usuarios
from empresa.views.empresa import (
    crear_empresa,
    listar_empresas,
)
from empresa.views.autenticacion import (
    registrar_usuario,
    login_usuario,
    logout_usuario,
)

# Reportes y contabilidad
from empresa.views.resumen import (
    resumen_financiero,
    estado_resultados,
)
from empresa.views.contabilidad import (
    balance_general,
    flujo_caja,
)
from empresa.views.dashboard import dashboard

# Exportaciones
from empresa.views.exportaciones import exportar_excel

urlpatterns = [
    # === Productos ===
    path('producto/crear/', crear_producto,        name='crear_producto'),
    path('producto/listar/', listar_productos,     name='listar_productos'),
    path('producto/info/',   obtener_info_producto, name='obtener_info_producto'),

    # === Ventas ===
    path('venta/crear/', crear_venta,   name='crear_venta'),
    path('venta/listar/', listar_ventas, name='listar_ventas'),

    # === Compras ===
    path('compra/crear/', crear_compra,   name='crear_compra'),
    path('compra/listar/', listar_compras, name='listar_compras'),

    # === Gastos ===
    path('gasto/crear/', crear_gasto,   name='crear_gasto'),
    path('gasto/listar/', listar_gastos, name='listar_gastos'),

    # === Capital ===
    path('capital/registrar/', crear_capital, name='registrar_capital'),
    path('capital/listar/',    listar_capital, name='listar_capital'),

    # === Cuentas Contables ===
    path('cuentas/crear/', crear_cuenta_contable,   name='crear_cuenta_contable'),
    path('cuentas/listar/', listar_cuentas_contables, name='listar_cuentas_contables'),

    # === Empresa y Usuarios ===
    path('empresa/crear/',  crear_empresa,   name='crear_empresa'),
    path('empresa/listar/', listar_empresas, name='listar_empresas'),
    path('registro/',       registrar_usuario, name='registro'),
    path('login/',          login_usuario,     name='login'),
    path('logout/',         logout_usuario,    name='logout'),

    # === Reportes y Dashboard ===
    path('resumen/',             resumen_financiero, name='resumen_financiero'),
    path('estado-resultados/',   estado_resultados,  name='estado_resultados'),
    path('balance-general/',     balance_general,    name='balance_general'),
    path('flujo-caja/',          flujo_caja,         name='flujo_caja'),
    path('dashboard/',           dashboard,          name='dashboard'),

    # === Exportaciones ===
    path('exportar/productos/', exportar_excel, name='exportar_excel_productos'),
]
