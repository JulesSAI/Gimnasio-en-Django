from django import forms
from .models import Sede, CatalogoEjercicios, Series, Repeticiones, Descanso, Entrenador, Usuario, Maquina, PerfilMedico, ClaseGrupal, Rutina, ReservaClase, SesionEntrenamiento, RutinaEjercicio

class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = '__all__'

class CatalogoEjerciciosForm(forms.ModelForm):
    class Meta:
        model = CatalogoEjercicios
        fields = '__all__'

class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'

class RepeticionesForm(forms.ModelForm):
    class Meta:
        model = Repeticiones
        fields = '__all__'

class DescansoForm(forms.ModelForm):
    class Meta:
        model = Descanso
        fields = '__all__'

class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'fecha_registro': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = '__all__'

class PerfilMedicoForm(forms.ModelForm):
    class Meta:
        model = PerfilMedico
        fields = '__all__'

class ClaseGrupalForm(forms.ModelForm):
    class Meta:
        model = ClaseGrupal
        fields = '__all__'
        widgets = {
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_hora_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = '__all__'

class ReservaClaseForm(forms.ModelForm):
    class Meta:
        model = ReservaClase
        fields = '__all__'
        widgets = {
            'fecha_hora_reserva': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class SesionEntrenamientoForm(forms.ModelForm):
    class Meta:
        model = SesionEntrenamiento
        fields = '__all__'
        widgets = {
            'fecha_hora_registro': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class RutinaEjercicioForm(forms.ModelForm):
    class Meta:
        model = RutinaEjercicio
        fields = '__all__'
