from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Libro
from .forms import LibroForm


class LibroListView(ListView):
    """Vista para listar todos los libros con paginación y búsqueda"""
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros'
    paginate_by = 10
    
    def get_queryset(self):
        """Filtra los libros según los parámetros de búsqueda"""
        queryset = Libro.objects.all()
        
        # Búsqueda por texto (título y autor)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(autor__icontains=search_query)
            )
        
        # Filtro por género
        genero = self.request.GET.get('genero')
        if genero:
            queryset = queryset.filter(genero=genero)
        
        return queryset.order_by('titulo', 'autor')
    
    def get_context_data(self, **kwargs):
        """Agrega contexto adicional para los filtros"""
        context = super().get_context_data(**kwargs)
        context['generos'] = Libro.GENERO_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['genero_selected'] = self.request.GET.get('genero', '')
        return context


class LibroDetailView(DetailView):
    """Vista para mostrar los detalles de un libro"""
    model = Libro
    template_name = 'libros/detalle_libro.html'
    context_object_name = 'libro'


class LibroCreateView(CreateView):
    """Vista para crear un nuevo libro"""
    model = Libro
    form_class = LibroForm
    template_name = 'libros/crear_libro.html'
    success_url = reverse_lazy('libros:lista')
    
    def form_valid(self, form):
        """Maneja el formulario válido"""
        messages.success(self.request, 'Libro creado exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Maneja el formulario inválido"""
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


class LibroUpdateView(UpdateView):
    """Vista para actualizar un libro existente"""
    model = Libro
    form_class = LibroForm
    template_name = 'libros/editar_libro.html'
    success_url = reverse_lazy('libros:lista')
    
    def form_valid(self, form):
        """Maneja el formulario válido"""
        messages.success(self.request, 'Libro actualizado exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Maneja el formulario inválido"""
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


class LibroDeleteView(DeleteView):
    """Vista para eliminar un libro"""
    model = Libro
    template_name = 'libros/confirmar_eliminar.html'
    success_url = reverse_lazy('libros:lista')
    
    def delete(self, request, *args, **kwargs):
        """Maneja la eliminación del libro"""
        messages.success(request, 'Libro eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


def home_view(request):
    """Vista principal del sistema"""
    # Libros recientes
    libros_recientes = Libro.objects.order_by('-fecha_ingreso')[:5]
    
    context = {
        'libros_recientes': libros_recientes,
    }
    
    return render(request, 'libros/home.html', context)
