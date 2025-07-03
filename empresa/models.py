from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de Empresa
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

# Usuario personalizado con empresa
class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.empresa})" if self.empresa else self.username

# Producto
class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

# Venta
class Venta(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta de {self.producto} - {self.total}"

# Compra
class Compra(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.producto} - {self.total}"

# Gasto
class Gasto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

# Movimiento Contable

class MovimientoContable(models.Model):
    empresa     = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cuenta_text = models.CharField(max_length=100)
    cuenta_fk   = models.ForeignKey(
        'CuentaContable',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='movimientos'
    )
    tipo        = models.CharField(
        max_length=10,
        choices=[('debito', 'Débito'), ('credito', 'Crédito')]
    )
    monto       = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField()
    fecha       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cuenta_fk or self.cuenta_text} - {self.tipo} - {self.monto}"

# Cuenta Contable
class CuentaContable(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('pasivo', 'Pasivo'), ('capital', 'Capital')])

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

# Capital
class Capital(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capital: {self.monto} - {self.empresa}"
