from django import forms
from .models import Empresa, Gasto, Venta, Producto, Compra, CuentaContable


# === FORMULARIO EMPRESA ===
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'ruc', 'direccion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if not ruc or not ruc.isdigit() or len(ruc) != 13:
            raise forms.ValidationError("El RUC debe tener exactamente 13 dígitos numéricos.")
        return ruc


# === FORMULARIO GASTO ===
class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        exclude = ['empresa']

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is None or monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto


# === FORMULARIO VENTA ===
class VentaForm(forms.ModelForm):
    def __init__(self, *args, empresa=None, **kwargs):
        self.empresa = empresa
        super().__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['total'].widget.attrs.update({
            'class': 'form-control',
            'readonly': 'readonly',
        })

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'total']  # <-- quitamos 'descripcion'

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or total <= 0:
            raise forms.ValidationError("El total debe ser mayor a cero.")
        return total

    def save(self, commit=True):
        instancia = super().save(commit=False)
        if self.empresa:
            instancia.empresa = self.empresa
        if commit:
            instancia.save()
        return instancia

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or total <= 0:
            raise forms.ValidationError("El total debe ser mayor a cero.")
        return total

    def save(self, commit=True):
        instancia = super().save(commit=False)
        if self.empresa:
            instancia.empresa = self.empresa
        if commit:
            instancia.save()
        return instancia

# === FORMULARIO PRODUCTO ===
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        exclude = ['empresa']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre

    def clean_codigo_barras(self):
        codigo = self.cleaned_data.get('codigo_barras')
        if not codigo or codigo.strip() == '':
            raise forms.ValidationError("El código de barras no puede estar vacío.")
        return codigo

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio unitario debe ser mayor a cero.")
        return precio


# === FORMULARIO COMPRA ===
class CompraForm(forms.ModelForm):
    def __init__(self, *args, empresa=None, **kwargs):
        self.empresa = empresa
        super().__init__(*args, **kwargs)
        # Asignar clases y readonly
        self.fields['producto'].widget.attrs.update({'class': 'form-select'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['total'].widget.attrs.update({
            'class': 'form-control',
            'readonly': 'readonly',
        })

    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'total']

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or total <= 0:
            raise forms.ValidationError("El total debe ser mayor a cero.")
        return total

    def save(self, commit=True):
        instancia = super().save(commit=False)
        if self.empresa:
            instancia.empresa = self.empresa
        if commit:
            instancia.save()
        return instancia

# === FORMULARIO CUENTA CONTABLE ===
class CuentaContableForm(forms.ModelForm):
    monto_inicial = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="💰 Monto inicial",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Saldo inicial de esta cuenta"
    )

    class Meta:
        model = CuentaContable
        fields = ['nombre', 'tipo']  # Sólo los campos del modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo':   forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, empresa=None, **kwargs):
        self.empresa = empresa
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # 1) Creo la cuenta contable
        cuenta = super().save(commit=False)
        if self.empresa:
            cuenta.empresa = self.empresa
        if commit:
            cuenta.save()
            # 2) Registro el movimiento contable de saldo inicial
            MovimientoContable.objects.create(
                empresa=self.empresa,
                cuenta=cuenta,
                tipo='debito',  # débito refleja un aumento de activo
                monto=self.cleaned_data['monto_inicial'],
                descripcion="Saldo inicial de la cuenta"
            )
        return cuenta


# === FORMULARIO CAPITAL ===
class CapitalForm(forms.Form):
    monto = forms.DecimalField(
        label="Monto del capital aportado",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empresa, Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Nombre (usuario)")
    last_name = forms.CharField(label="Apellidos")
    # Campos de empresa:
    nombre_empresa = forms.CharField(max_length=100, label="🏢 Nombre de la empresa")
    ruc = forms.CharField(max_length=13, label="📇 RUC de la empresa")
    direccion = forms.CharField(max_length=200, label="📍 Dirección de la empresa")

    class Meta:
        model = Usuario
        # OJO: aquí "nombre_empresa" no es atributo de Usuario, lo usaremos
        # para crear la Empresa. Por eso lo excluimos del model y lo manejamos manual.
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'password1', 'password2',
            'nombre_empresa', 'ruc', 'direccion',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplico form-control a todos los widgets:
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        # 1) Creo primero la empresa
        empresa = Empresa(
            nombre=self.cleaned_data['nombre_empresa'],
            ruc=self.cleaned_data['ruc'],
            direccion=self.cleaned_data['direccion']
        )
        if commit:
            empresa.save()

        # 2) Creo el usuario y le asigno la empresa
        usuario = super().save(commit=False)
        usuario.empresa = empresa
        if commit:
            usuario.save()
        return usuario
