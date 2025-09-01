# Gestor de Libros

Sistema simple para gestionar una biblioteca personal desarrollado con Django.

## Características

-  **CRUD de libros**: Crear, ver, editar y eliminar
-  **Búsqueda**: Por título, autor y género
-  **Responsive**: Funciona en móvil y computadora
-  **Interfaz moderna**: Diseño limpio con Bootstrap

## Uso

- **Inicio** (`/`): Página principal
- **Libros** (`/libros/`): Ver todos los libros
- **Crear** (`/libros/crear/`): Agregar nuevo libro
- **Admin** (`/admin/`): Panel de administración

##  Tecnologías

- **Backend**: Django 4.2.7
- **Base de datos**: MySQL/MariaDB
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Python**: 3.12+

## Estructura

```
Gestor_libros/
├── Gestor_libros/     # Configuración Django
├── libros/            # Aplicación principal
├── templates/         # Plantillas HTML
└── manage.py         # Comandos Django
```

## Comandos Útiles

```bash
python manage.py runserver    # Ejecutar servidor
python manage.py createsuperuser  # Crear admin
python manage.py check        # Verificar proyecto
```

**Desarrollado con Django y Python**
**REQUERIMENTOS
Django==4.2.7
PyMySQL==1.1.2
sqlparse==0.5.3
asgiref==3.9.1
tzdata==2025.2
