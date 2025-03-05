from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    listar_usuarios_ad, EmpresaViewSet, SedeViewSet, EmpresaSedeViewSet, 
    AreaViewSet, DepartamentoViewSet, UsuarioViewSet, EstadoViewSet, 
    EquipoViewSet, ContratoViewSet, HistorialAsignacionesViewSet
)

# 📌 Rutas automáticas para los ViewSets
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'empresa-sedes', EmpresaSedeViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'contratos', ContratoViewSet)
router.register(r'historial-asignaciones', HistorialAsignacionesViewSet)

# 📌 Rutas personalizadas
urlpatterns = [
    path('api/', include(router.urls)),  # Incluye todas las rutas de los ViewSets
    path('api/listar-usuarios-ad/', listar_usuarios_ad, name='listar_usuarios_ad'),  # Endpoint para listar usuarios del AD
]
