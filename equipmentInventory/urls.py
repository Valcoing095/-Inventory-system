from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EmpresaViewSet, SedeViewSet, EmpresaSedeViewSet, AreaViewSet, 
                    DepartamentoViewSet, UsuarioViewSet, EquipoViewSet, 
                    ContratoViewSet, listar_usuarios_ad)

# 🔹 Router para los ViewSets (CRUD Automático con Django REST Framework)
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'empresa-sedes', EmpresaSedeViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'usuarios', UsuarioViewSet)
# router.register(r'estados', EstadoViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'contratos', ContratoViewSet)
# router.register(r'historial-asignaciones', HistorialAsignacionesViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # 🔹 API REST para CRUD de todas las entidades
    path('api/usuarios/carga_masiva_usuarios/', UsuarioViewSet.as_view({'post': 'carga_masiva_usuarios'}), name='carga_masiva_usuarios'),
    path('api/equipos/carga_masiva_equipos/', EquipoViewSet.as_view({'post': 'carga_masiva_equipos'}), name='carga_masiva_equipos'),
    path('api/usuarios-ad/', listar_usuarios_ad, name='listar_usuarios_ad'),
]
