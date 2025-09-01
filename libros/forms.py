from django import forms
from django.core.exceptions import ValidationError
from .models import Libro


class LibroForm(forms.ModelForm):
    """Formulario para crear y editar libros"""
    
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'genero', 'año_publicacion'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del libro',
                'required': True
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del autor',
                'required': True
            }),
            'genero': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'año_publicacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año de publicación',
                'min': '1000',
                'max': '2024',
                'required': True
            }),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'genero': 'Género',
            'año_publicacion': 'Año de Publicación',
        }
        help_texts = {
            'año_publicacion': 'Año en que fue publicado el libro',
        }
    
    def clean_año_publicacion(self):
        """Valida el año de publicación"""
        año = self.cleaned_data.get('año_publicacion')
        
        if año:
            if año < 1000 or año > 2024:
                raise ValidationError('El año de publicación debe estar entre 1000 y 2024.')
        
        return año


class BusquedaLibroForm(forms.Form):
    """Formulario para búsqueda de libros"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título o autor...',
            'id': 'search-input'
        }),
        label='Búsqueda'
    )
    
    genero = forms.ChoiceField(
        choices=[('', 'Todos los géneros')] + list(Libro.GENERO_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'genero-filter'
        }),
        label='Género'
    )
