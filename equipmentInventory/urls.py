from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, SedeViewSet, EmpresaSedeViewSet, AreaViewSet, AreaSedeViewSet, DepartamentoViewSet, UsuarioViewSet, EstadoViewSet, EquipoViewSet, HistorialAsignacionesViewSet

# Creamos un enrutador para los ViewSets
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'empresa-sedes', EmpresaSedeViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'area-sedes', AreaSedeViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'historial-asignaciones', HistorialAsignacionesViewSet)

# Incluimos las rutas en la configuración de Django
urlpatterns = [
    path('api/', include(router.urls)),
]
