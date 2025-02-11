from rest_framework import viewsets
from .models import Empresa, Sede, EmpresaSede, Area, AreaSede, Departamento, Usuario, Estado, Equipo, HistorialAsignaciones
from .serializers import EmpresaSerializer, SedeSerializer, EmpresaSedeSerializer, AreaSerializer, AreaSedeSerializer, DepartamentoSerializer, UsuarioSerializer, EstadoSerializer, EquipoSerializer, HistorialAsignacionesSerializer

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

class AreaSedeViewSet(viewsets.ModelViewSet):
    queryset = AreaSede.objects.all()
    serializer_class = AreaSedeSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
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
