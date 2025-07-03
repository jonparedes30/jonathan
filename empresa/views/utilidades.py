from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_ruc(ruc):
    """Valida un RUC ecuatoriano simple (solo longitud y tipo numérico)"""
    if not ruc.isdigit() or len(ruc) != 13:
        raise ValidationError(_('El RUC debe contener 13 dígitos numéricos.'))

def redondear_decimal(valor, decimales=2):
    """Redondea valores numéricos a N decimales"""
    try:
        return round(float(valor), decimales)
    except (TypeError, ValueError):
        return 0.00

def formato_moneda(valor):
    """Devuelve un valor con formato monetario"""
    return "${:,.2f}".format(valor)
