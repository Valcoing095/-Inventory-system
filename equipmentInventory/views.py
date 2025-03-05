from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from ldap3 import Server, Connection, ALL
from django.conf import settings
from rest_framework import status

from .models import (Contrato, Empresa, Sede, EmpresaSede, Area, Departamento, 
                     Usuario, Estado, Equipo, HistorialAsignaciones)
from .serializers import (ContratoSerializer, EmpresaSerializer, SedeSerializer, EmpresaSedeSerializer, 
                          AreaSerializer, DepartamentoSerializer, UsuarioSerializer, EstadoSerializer, 
                          EquipoSerializer, HistorialAsignacionesSerializer)


# 🔹 ViewSets para CRUD con Django REST Framework (DRF)
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
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

class HistorialAsignacionesViewSet(viewsets.ModelViewSet):
    queryset = HistorialAsignaciones.objects.all()
    serializer_class = HistorialAsignacionesSerializer


# Configuración del servidor LDAP
LDAP_SERVER = "172.16.2.5"  # Asegúrate de que sea una cadena
LDAP_USER = "CN=caminos\\adm_yvelascot,CN=Users,DC=caminos,DC=com"  # Asegúrate de que sea una cadena
LDAP_PASSWORD = "Caminos2021"  # Asegúrate de que sea una cadena
BASE_DN = "DC=caminos,DC=com"  # Dominio base de búsqueda
FILTER = "(objectClass=user)"  # Filtro para listar solo usuarios

@api_view(["GET"])
def listar_usuarios_ad(request):
    """
    Retorna una lista de usuarios del Active Directory.
    """
    try:
        # Crear el objeto Server
        server = Server(LDAP_SERVER, get_info=ALL)

        # Crear la conexión
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)
        print("✅ Conexión exitosa al Active Directory")

        # Realizar la búsqueda de usuarios
        conn.search(BASE_DN, FILTER, attributes=['cn', 'mail'])

        # Obtener los resultados
        usuarios = []
        for entry in conn.entries:
            usuarios.append({
                "nombre": entry.cn.value,
                "correo": entry.mail.value if hasattr(entry, 'mail') else None
            })

        # Cerrar la conexión
        conn.unbind()

        # Retornar la lista de usuarios
        return Response({"usuarios": usuarios}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)