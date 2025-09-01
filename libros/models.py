from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Libro(models.Model):
    """Modelo para representar un libro en el sistema"""
    
    GENERO_CHOICES = [
        ('ficcion', 'Ficción'),
        ('no_ficcion', 'No Ficción'),
        ('ciencia', 'Ciencia'),
        ('historia', 'Historia'),
        ('biografia', 'Biografía'),
        ('tecnologia', 'Tecnología'),
        ('arte', 'Arte'),
        ('deportes', 'Deportes'),
        ('otros', 'Otros'),
    ]
    
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título",
        help_text="Título del libro"
    )
    autor = models.CharField(
        max_length=100, 
        verbose_name="Autor",
        help_text="Nombre del autor"
    )
    genero = models.CharField(
        max_length=20,
        choices=GENERO_CHOICES,
        default='otros',
        verbose_name="Género"
    )
    año_publicacion = models.PositiveIntegerField(
        verbose_name="Año de Publicación",
        validators=[MinValueValidator(1000), MaxValueValidator(2024)],
        help_text="Año de publicación del libro"
    )
    fecha_ingreso = models.DateField(
        auto_now_add=True,
        verbose_name="Fecha de Ingreso"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo', 'autor']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['autor']),
            models.Index(fields=['genero']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"
    
    def get_absolute_url(self):
        """Retorna la URL para ver los detalles del libro"""
        return reverse('libros:detalle', kwargs={'pk': self.pk})
