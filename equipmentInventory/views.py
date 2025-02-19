from rest_framework import viewsets
from .models import Empresa, Sede, EmpresaSede, Area, Departamento, Usuario, Estado, Equipo, HistorialAsignaciones
from .serializers import EmpresaSerializer, SedeSerializer, EmpresaSedeSerializer, AreaSerializer, DepartamentoSerializer, UsuarioSerializer, EstadoSerializer, EquipoSerializer, HistorialAsignacionesSerializer
'''
    En Django para manejar los eventos del CRUD usando el DRF(orm de django) se usa el ModelViewset

    Este ModelViewSet automáticamente gestiona:

    GET /api/usuarios/ → Lista todos los usuarios.
    GET /api/usuarios/1/ → Obtiene un usuario específico.
    POST /api/usuarios/ → Crea un usuario (Lanza la validación y guarda el registro).
    PUT /api/usuarios/1/ → Actualiza un usuario.
    DELETE /api/usuarios/1/ → Elimina un usuario.


'''
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer

class EmpresaSedeViewSet(viewsets.ModelViewSet):
    queryset = EmpresaSede.objects.all()
    serializer_class = EmpresaSedeSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset =Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class HistorialAsignacionesViewSet(viewsets.ModelViewSet):
    queryset = HistorialAsignaciones.objects.all()
    serializer_class = HistorialAsignacionesSerializer
