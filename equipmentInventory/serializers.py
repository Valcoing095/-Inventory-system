from rest_framework import serializers
from .models import Empresa, Sede, EmpresaSede, Area, Departamento, Usuario, Estado, Equipo, HistorialAsignaciones,Contrato

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class EmpresaSedeSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source="empresa.nombre")
    sede_nombre = serializers.CharField(source="sede.nombre")
    class Meta:
        model = EmpresaSede
        fields = ["id",
            "empresa",
            "empresa_nombre",
            "sede",
            "sede_nombre"
        ]

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source="departamento.nombre", read_only=True)
    area = serializers.CharField(source="departamento.area.nombre", read_only=True)
    empresa_nombre=serializers.CharField(source="empresa_sede.empresa.nombre", read_only=True)
    sede_nombre = serializers.CharField(source="empresa_sede.sede.nombre", read_only=True)

    dominios= ["caminos.com.co","sanoysalvo.com.co","andinautos.com.co"]

    # Para validar los campos django usa por defecto el validate_nombre del campo
    def validate_correo(self,value):
        # Validar si el correo es corporativo de grupo caminos
         
        dominio = value.split("@")[-1]  # Extrae el dominio del correo
        if dominio not in self.dominios:
            raise serializers.ValidationError(f"El correo debe pertenecer a: {', '.join(self.dominios)}")
        return value

    class Meta:
        model = Usuario
        fields = [
            "id", "nombre", "cargo", "correo", "username_ad", 
            "departamento",  # Campo escribible
            "departamento_nombre", "area","empresa_sede","empresa_nombre","sede_nombre"   # Campos de solo lectura
        ]
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'



from ldap3 import Server, Connection, ALL




LDAP_SERVER = "172.16.2.5"
LDAP_USER = "CN=Yeison Alexis Velasco Trejos,ou=Adm_sistemas,DC=caminos,DC=com"
LDAP_PASSWORD = "Caminos2021"
BASE_DN = "DC=caminos,DC=com"
FILTER = "(objectClass=user)"
class EquipoSerializer(serializers.ModelSerializer):
    contrato_proveedor = serializers.CharField(source="contrato.proveedor", read_only=True)
    contrato_numero = serializers.CharField(source="contrato.num_contrato", read_only=True)
    usuario_info = serializers.SerializerMethodField()  # Se agregará la información del usuario AD

    class Meta:
        model = Equipo
        fields = [
            "id", "serial", "modelo", "marca", "tipo", "costo_unitario",
            "contrato", "contrato_proveedor", "contrato_numero", "usuario", "nombre", "usuario_info"
        ]

    def get_usuario_info(self, obj):
        """Busca la información del usuario en Active Directory."""
        if not obj.usuario:
            return None  # Si no hay usuario, retornar None

        user_ad = obj.usuario  # Se asume que `usuario` almacena el `user_AD`
        
        try:
            server = Server(LDAP_SERVER, get_info=ALL)
            conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

            filtro = f"(sAMAccountName={user_ad})"
            conn.search(BASE_DN, filtro, attributes=['cn', 'mail', 'sAMAccountName', 'department', 'company'])

            if conn.entries:
                entry = conn.entries[0]  # Tomamos el primer resultado
                return {
                    "nombre": entry.cn.value,
                    "correo": entry.mail.value if hasattr(entry, 'mail') else None,
                    "user_AD": entry.sAMAccountName.value,
                    "departamento": entry.department.value if hasattr(entry, 'department') else None,
                    "empresa": entry.company.value if hasattr(entry, 'company') else None
                }
            
            return None  # Si no hay coincidencias en AD

        except Exception as e:
            return {"error": str(e)}

class HistorialAsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAsignaciones
        fields = '__all__'
