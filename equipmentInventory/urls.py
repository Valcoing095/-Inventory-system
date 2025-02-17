from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, SedeViewSet, EmpresaSedeViewSet, AreaViewSet, DepartamentoViewSet, UsuarioViewSet, EstadoViewSet, EquipoViewSet, HistorialAsignacionesViewSet

# Configurar Router para los ViewSets
router = DefaultRouter()
router.register(r"empresas", EmpresaViewSet)
router.register(r"sedes", SedeViewSet)
router.register(r"empresa-sedes", EmpresaSedeViewSet)
router.register(r"areas", AreaViewSet)
router.register(r"departamentos", DepartamentoViewSet)
router.register(r"usuarios", UsuarioViewSet)
router.register(r"estados", EstadoViewSet)
router.register(r"equipos", EquipoViewSet)
router.register(r"historial-asignaciones", HistorialAsignacionesViewSet)

urlpatterns = [
    path("api/", include(router.urls)),  # Rutas automáticas para los modelos
]
