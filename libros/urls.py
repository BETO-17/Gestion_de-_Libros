from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    # Vista principal
    path('', views.home_view, name='home'),
    
    # CRUD de libros
    path('libros/', views.LibroListView.as_view(), name='lista'),
    path('libros/crear/', views.LibroCreateView.as_view(), name='crear'),
    path('libros/<int:pk>/', views.LibroDetailView.as_view(), name='detalle'),
    path('libros/<int:pk>/editar/', views.LibroUpdateView.as_view(), name='editar'),
    path('libros/<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='eliminar'),
    
    # API endpoints
    path('api/libros/<int:pk>/cambiar-estado/', views.cambiar_estado_libro, name='cambiar_estado'),
]
