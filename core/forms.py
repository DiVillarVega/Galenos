from django import forms
from django.forms import ModelForm, Form, Textarea, FileInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria, Producto, Bodega,Perfil

# *********************************************************************************************************#
#                                                                                                          #
# INSTRUCCIONES PARA EL ALUMNO, PUEDES SEGUIR EL VIDEO TUTORIAL, COMPLETAR EL CODIGO E INCORPORAR EL TUYO: #
#                                                                                                          #
# https://drive.google.com/drive/folders/1ObwMnpKmCXVbq3SMwJKlSRE0PCn0buk8?usp=drive_link                  #
#                                                                                                          #
# *********************************************************************************************************#

# PARA LA PAGINA MANTENEDOR DE PRODUCTOS:
# Crea ProductoForm como una clase que hereda de ModelForm
# asocialo con el modelo Producto
# muestra todos los campos
# crea 2 widgets para:
#   - la descripción del producto como TextArea
#   - el botón de cargar imagen como FileInput y 
#     escóndelo para reemplazarlo por otro acorde 
#     con tu diseño gráfico
# renombra las siguientes etiquetas para que ocupen menos
# espacio en la página: 'Nombre', 'Subscriptor(%)' y 'Oferta(%)'
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(),
            'imagen': forms.FileInput()        
        }
        labels = {
            'nombre': 'Nombre',
            'descuento_subscriptor': 'Subscriptor(%)',
            'descuento_oferta': 'Oferta(%)'
        }

# El formulario de bodega está listo, no necesitas modificarlo
class BodegaForm(Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría')
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), label='Producto')
    cantidad = forms.IntegerField(label='Cantidad')
    class Meta:
        fields = '__all__'

# El formulario de ingreso está listo, no necesitas modificarlo
class IngresarForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'username'
        }),
        label="Cuenta"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'password'
        }),
        label="Contraseña"
    )
    
    class Meta:
        fields = ['username', 'password']

# PARA LA PAGINA DE REGISTRO DE NUEVO CLIENTE:
# Crea RegistroUsuarioForm como una clase que hereda de UserCreationForm
# asocialo con el modelo User
# muestra los campos: 
#    'username', 'first_name', 'last_name', 'email', 'password1' y 'password2'
# renombra la etiqueta del campo 'email' por 'E-mail'

# class RegistroUsuarioForm(UserCreationForm):
#    class Meta:
#         model = User
#         fields = '__all__'

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'username'
        }),
        label="RUT"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'first_name'
        }),
        label="Nombre"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'last_name'
        }),
        label="Apellido"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'email'
        }),
        label="Correo electrónico"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'password1'
        }),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'required': True,
            'name': 'password2'
        }),
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class RegistroPerfilForm(forms.ModelForm):

    direccion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input',
            'required': True,
            'name': 'direccion',
            'id': 'id_direccion'
        }),
        label="Dirección"
    )
    subscrito = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'input',
            'required': False,
            'name': 'subscrito'
        }),
        label="Subscrito"
    )


    class Meta:
        model = Perfil 
        fields = ['direccion', 'subscrito']
        exclude = ['tipo_usuario']
        widgets = {
            'direccion': forms.Textarea()
        }




# PARA LA PAGINA MIS DATOS Y MANTENEDOR DE USUARIOS:
# Crear UsuarioForm como una clase que hereda de ModelForm
# asocialo con el modelo User
# muestra todos los campos: 'username', 'first_name', 'last_name' e 'email'
# renombra la etiqueta del campo 'email' por 'E-mail'
class UsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'email': 'E-mail',
            'username': 'RUT',
            'first_name': 'Nombre',
            'last_name': 'Apellidos'
        }

# PARA LA PAGINA MANTENEDOR DE USUARIOS:
# Crear PerfilForm como una clase que hereda de ModelForm
# asocialo con el modelo Perfil
# muestra todos los campos: 
#    'tipo_usuario', 'rut', 'direccion', 'subscrito'e 'imagen'
# crea los widgets para:
#   - direccion como Textarea,
#   - imagen como FileInput()
class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario', 'direccion', 'subscrito']
        widgets = {
            'direccion': Textarea(attrs={'cols': 80, 'rows': 20})
        }
