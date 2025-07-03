from django.db import models
from .empresa import Empresa  # Ajusta si tu modelo Empresa está en otro archivo

class Meta(models.Model):
    TIPO_CHOICES = [
        ('ventas', 'Ventas'),
        ('utilidad', 'Utilidad'),
        ('ahorro', 'Ahorro'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    objetivo_mensual = models.DecimalField(max_digits=12, decimal_places=2)
    mes = models.IntegerField()  # 1 = enero, 12 = diciembre
    anio = models.IntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empresa} - {self.get_tipo_display()} {self.mes}/{self.anio}"
