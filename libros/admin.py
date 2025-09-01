from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Libro
from django.utils import timezone


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Libro"""
    
    list_display = [
        'titulo', 'autor', 'genero', 'año_publicacion', 
        'fecha_ingreso', 'acciones'
    ]
    
    list_filter = [
        'genero', 'año_publicacion', 'fecha_ingreso'
    ]
    
    search_fields = [
        'titulo', 'autor'
    ]
    
    list_per_page = 25
    list_max_show_all = 100
    
    readonly_fields = [
        'fecha_ingreso', 'fecha_modificacion'
    ]
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['titulo', 'autor', 'genero']
        }),
        ('Detalles de Publicación', {
            'fields': ['año_publicacion']
        }),
        ('Información del Sistema', {
            'fields': ['fecha_ingreso', 'fecha_modificacion'],
            'classes': ['collapse']
        }),
    ]
    
    def acciones(self, obj):
        """Muestra botones de acción en la lista"""
        if obj.pk:
            edit_url = reverse('admin:libros_libro_change', args=[obj.pk])
            view_url = reverse('libros:detalle', args=[obj.pk])
            
            return format_html(
                '<a class="button" href="{}" title="Editar">✏️</a> '
                '<a class="button" href="{}" title="Ver en sitio" target="_blank">👁️</a>',
                edit_url, view_url
            )
        return '-'
    
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True
    
    def get_queryset(self, request):
        """Optimiza las consultas del admin"""
        return super().get_queryset(request).select_related()
    
    def save_model(self, request, obj, form, change):
        """Personaliza el guardado del modelo"""
        if not change:  # Si es un nuevo libro
            obj.fecha_ingreso = obj.fecha_ingreso or timezone.now().date()
        super().save_model(request, obj, form, change)
    
    # Personalización de la interfaz
    def get_list_display(self, request):
        """Personaliza la lista según el usuario"""
        if request.user.is_superuser:
            return self.list_display
        else:
            # Para usuarios no superusuarios, ocultar algunos campos
            return [
                'titulo', 'autor', 'genero', 'año_publicacion', 'fecha_ingreso'
            ]
    
    def has_delete_permission(self, request, obj=None):
        """Controla los permisos de eliminación"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Controla los permisos de edición"""
        return True
    
    def has_add_permission(self, request):
        """Controla los permisos de creación"""
        return True


# Configuración del sitio admin
admin.site.site_header = "Administración del Sistema de Libros"
admin.site.site_title = "Gestor de Libros"
admin.site.index_title = "Panel de Control - Gestión de Libros"
