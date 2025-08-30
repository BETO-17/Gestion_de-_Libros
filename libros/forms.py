from django import forms
from django.core.exceptions import ValidationError
from .models import Libro


class LibroForm(forms.ModelForm):
    """Formulario para crear y editar libros"""
    
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'isbn', 'genero', 'editorial',
            'año_publicacion', 'paginas', 'descripcion', 'estado'
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
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el código ISBN (13 dígitos)',
                'maxlength': '13',
                'required': True
            }),
            'genero': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'editorial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la editorial (opcional)'
            }),
            'año_publicacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año de publicación',
                'min': '1000',
                'max': '2024',
                'required': True
            }),
            'paginas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de páginas (opcional)',
                'min': '1'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del libro (opcional)',
                'rows': '4'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'genero': 'Género',
            'editorial': 'Editorial',
            'año_publicacion': 'Año de Publicación',
            'paginas': 'Número de Páginas',
            'descripcion': 'Descripción',
            'estado': 'Estado',
        }
        help_texts = {
            'isbn': 'Código ISBN de 13 dígitos único para el libro',
            'año_publicacion': 'Año en que fue publicado el libro',
            'descripcion': 'Breve descripción del contenido del libro',
        }
    
    def clean_isbn(self):
        """Valida el formato del ISBN"""
        isbn = self.cleaned_data.get('isbn')
        
        if isbn:
            # Remover espacios y guiones
            isbn = isbn.replace(' ', '').replace('-', '')
            
            # Verificar que solo contenga dígitos
            if not isbn.isdigit():
                raise ValidationError('El ISBN debe contener solo números.')
            
            # Verificar longitud
            if len(isbn) != 13:
                raise ValidationError('El ISBN debe tener exactamente 13 dígitos.')
        
        return isbn
    
    def clean_año_publicacion(self):
        """Valida el año de publicación"""
        año = self.cleaned_data.get('año_publicacion')
        
        if año:
            if año < 1000 or año > 2024:
                raise ValidationError('El año de publicación debe estar entre 1000 y 2024.')
        
        return año
    
    def clean_paginas(self):
        """Valida el número de páginas"""
        paginas = self.cleaned_data.get('paginas')
        
        if paginas is not None and paginas <= 0:
            raise ValidationError('El número de páginas debe ser mayor a 0.')
        
        return paginas


class BusquedaLibroForm(forms.Form):
    """Formulario para búsqueda de libros"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, autor, ISBN o editorial...',
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
    
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + list(Libro.ESTADO_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'estado-filter'
        }),
        label='Estado'
    )
