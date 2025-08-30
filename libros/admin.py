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
        'titulo', 'autor', 'isbn', 'genero', 'estado', 
        'año_publicacion', 'editorial', 'fecha_ingreso', 'acciones'
    ]
    
    list_filter = [
        'genero', 'estado', 'año_publicacion', 'fecha_ingreso', 
        'editorial'
    ]
    
    search_fields = [
        'titulo', 'autor', 'isbn', 'editorial', 'descripcion'
    ]
    
    list_per_page = 25
    list_max_show_all = 100
    
    readonly_fields = [
        'fecha_ingreso', 'fecha_modificacion'
    ]
    
    fieldsets = [
        ('Información Básica', {
            'fields': ['titulo', 'autor', 'isbn', 'genero']
        }),
        ('Detalles de Publicación', {
            'fields': ['editorial', 'año_publicacion', 'paginas']
        }),
        ('Contenido', {
            'fields': ['descripcion'],
            'classes': ['collapse']
        }),
        ('Estado del Sistema', {
            'fields': ['estado', 'fecha_ingreso', 'fecha_modificacion'],
            'classes': ['collapse']
        }),
    ]
    
    actions = [
        'marcar_como_disponible',
        'marcar_como_prestado',
        'marcar_como_reservado',
        'marcar_como_perdido'
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
    
    # Acciones personalizadas
    def marcar_como_disponible(self, request, queryset):
        """Marca los libros seleccionados como disponibles"""
        updated = queryset.update(estado='disponible')
        self.message_user(
            request, 
            f'{updated} libro(s) marcado(s) como disponible(s).'
        )
    marcar_como_disponible.short_description = "Marcar como disponible"
    
    def marcar_como_prestado(self, request, queryset):
        """Marca los libros seleccionados como prestados"""
        updated = queryset.update(estado='prestado')
        self.message_user(
            request, 
            f'{updated} libro(s) marcado(s) como prestado(s).'
        )
    marcar_como_prestado.short_description = "Marcar como prestado"
    
    def marcar_como_reservado(self, request, queryset):
        """Marca los libros seleccionados como reservados"""
        updated = queryset.update(estado='reservado')
        self.message_user(
            request, 
            f'{updated} libro(s) marcado(s) como reservado(s).'
        )
    marcar_como_reservado.short_description = "Marcar como reservado"
    
    def marcar_como_perdido(self, request, queryset):
        """Marca los libros seleccionados como perdidos"""
        updated = queryset.update(estado='perdido')
        self.message_user(
            request, 
            f'{updated} libro(s) marcado(s) como perdido(s).'
        )
    marcar_como_perdido.short_description = "Marcar como perdido"
    
    # Personalización de la interfaz
    def get_list_display(self, request):
        """Personaliza la lista según el usuario"""
        if request.user.is_superuser:
            return self.list_display
        else:
            # Para usuarios no superusuarios, ocultar algunos campos
            return [
                'titulo', 'autor', 'isbn', 'genero', 'estado', 
                'año_publicacion', 'fecha_ingreso'
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
