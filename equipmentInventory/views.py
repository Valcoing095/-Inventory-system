from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

from .models import (Contrato, Empresa, Sede, EmpresaSede, Area, Departamento, 
                     Usuario, Estado, Equipo, HistorialAsignaciones)
from .serializers import (ContratoSerializer, EmpresaSerializer, SedeSerializer, EmpresaSedeSerializer, 
                          AreaSerializer, DepartamentoSerializer, UsuarioSerializer, EstadoSerializer, 
                          EquipoSerializer, HistorialAsignacionesSerializer)
from django.db import transaction


# ===========================
# 📌 CRUD de Empresas, Sedes, Áreas y Departamentos
# ===========================
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

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


# ===========================
# 📌 CRUD de Usuarios con Carga Masiva
# ===========================
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['post'])
    def carga_masiva_usuarios(self, request):
        """
        Carga masiva de usuarios desde un archivo Excel (.xlsx).
        """
        try:
            archivo = request.FILES.get('archivo')
            if not archivo:
                return Response({"error": "No se encontró el archivo"}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(archivo)

            # Validar columnas requeridas
            columnas_requeridas = {"nombre", "correo", "cargo", "username_ad", "empresa_sede", "departamento"}
            if not columnas_requeridas.issubset(df.columns):
                return Response({"error": f"El archivo debe contener las siguientes columnas: {', '.join(columnas_requeridas)}"}, status=status.HTTP_400_BAD_REQUEST)

            usuarios_creados = []
            errores = []

            for _, row in df.iterrows():
                try:
                    empresa_sede = EmpresaSede.objects.get(id=row["empresa_sede"]) if pd.notna(row["empresa_sede"]) else None
                    departamento = Departamento.objects.get(id=row["departamento"]) if pd.notna(row["departamento"]) else None

                    usuario = Usuario(
                        nombre=row["nombre"],
                        correo=row["correo"],
                        cargo=row["cargo"],
                        username_ad=row["username_ad"],
                        empresa_sede=empresa_sede,
                        departamento=departamento,
                    )
                    usuario.save()
                    usuarios_creados.append(usuario.nombre)

                except ObjectDoesNotExist as e:
                    errores.append(f"Error con el usuario {row['nombre']}: {str(e)}")

            return Response({
                "mensaje": f"{len(usuarios_creados)} usuarios creados correctamente.",
                "errores": errores
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    @action(detail=False, methods=['post'])
    def carga_masiva_equipos(self, request):
        """
        Carga masiva de equipos desde un archivo Excel (.xlsx).
        """
        try:
            archivo = request.FILES.get('archivo')
            if not archivo:
                return Response({"error": "No se encontró el archivo"}, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(archivo)

            print(df)
            # Validar columnas requeridas
            columnas_requeridas = {"serial", "modelo", "tipo", "marca", "procesador", "disco_duro", "ram", 
                                   "proveedor", "costo_unitario", "usuario", "contrato"}
            if not columnas_requeridas.issubset(df.columns):
                return Response({"error": f"El archivo debe contener las siguientes columnas: {', '.join(columnas_requeridas)}"}, 
                                status=status.HTTP_400_BAD_REQUEST)

            equipos_creados = []
            errores = []

            print("\n📢 **Iniciando carga masiva de equipos...**\n")

            for _, row in df.iterrows():
                try:
                    print(f"🔹 Procesando equipo: {row['serial']} - {row['modelo']}...")

                    usuario = Usuario.objects.get(id=row["usuario"]) if pd.notna(row["usuario"]) else None
                    
                    contrato = Contrato.objects.get(num_contrato=row["contrato"]) if pd.notna(row["contrato"]) else None

                    # 📌 Realizar la transacción individualmente
                    with transaction.atomic():
                        equipo = Equipo(
                            serial=row["serial"],
                            modelo=row["modelo"],
                            tipo=row["tipo"],
                            marca=row["marca"],
                            procesador=row["procesador"],
                            disco_duro=row["disco_duro"],
                            ram=row["ram"],
                            proveedor=row["proveedor"],
                            costo_unitario=row["costo_unitario"],
                            usuario=usuario,
                            contrato=contrato,
                        )
                        equipo.save()
                        equipos_creados.append(equipo.serial)
                        print(f"✅ Equipo guardado: {equipo.serial} - {equipo.modelo}")

                except ObjectDoesNotExist as e:
                    error_msg = f"❌ Error con el equipo {row['serial']}: {str(e)}"
                    errores.append(error_msg)
                    print(error_msg)

                except Exception as e:
                    error_msg = f"❌ Error inesperado con el equipo {row['serial']}: {str(e)}"
                    errores.append(error_msg)
                    print(error_msg)

            print("\n📢 **Carga masiva finalizada**\n")
            print(f"✅ Total equipos creados: {len(equipos_creados)}")
            print(f"⚠️ Total errores: {len(errores)}")

            return Response({
                "mensaje": f"{len(equipos_creados)} equipos creados correctamente.",
                "errores": errores
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"❌ Error crítico: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ===========================
# 📌 Configuración LDAP
# ===========================
from ldap3 import Server, Connection, ALL

LDAP_SERVER = "172.16.2.5"
LDAP_USER = "CN=Yeison Alexis Velasco Trejos,ou=Adm_sistemas,DC=caminos,DC=com"
LDAP_PASSWORD = "Caminos2021"
BASE_DN = "DC=caminos,DC=com"
FILTER = "(objectClass=user)"

@api_view(["GET"])
def listar_usuarios_ad(request):
    """
    Retorna una lista de usuarios del Active Directory.
    """
    try:
        # Conectar con el servidor LDAP
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

        # Buscar usuarios en Active Directory
        conn.search(BASE_DN, FILTER, attributes=['cn', 'mail','sAMAccountName','distinguishedName'])

        # Extraer los resultados
    
        usuarios = [
            {
                "nombre": entry.cn.value,
                "correo": entry.mail.value if hasattr(entry, 'mail') else None,
                "user AD": entry.sAMAccountName.value,
                "Ubicación usuario": entry.distinguishedName.value
            }
            for entry in conn.entries
        ]

        conn.unbind()

        return Response({"usuarios": usuarios}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
