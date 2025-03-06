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

class EquipoSerializer(serializers.ModelSerializer):
    usuario_name =  serializers.SerializerMethodField()
    sede_nombre = serializers.CharField(source="usuario.empresa_sede.sede.nombre", read_only=True)
    empresa_nombre = serializers.CharField(source="usuario.empresa_sede.empresa.nombre", read_only=True)
    contrato_proveedor = serializers.CharField(source="contrato.proveedor", read_only=True)
    contrato_numero =  serializers.CharField(source="contrato.num_contrato",read_only=True)

    class Meta:
        model = Equipo
        fields = ["id","serial", "modelo", "marca", "tipo","costo_unitario", "usuario", "usuario_name", "sede_nombre","empresa_nombre","contrato","contrato_proveedor","contrato_numero"]

    def get_usuario_name(self, obj):
        """
        Retorna la empresa asociada a la sede del usuario.
        Como la relación es Many-to-Many, tomamos la primera empresa asociada a la sede.
        """
        if obj.usuario:
            usuario_name = obj.usuario.nombre
            return usuario_name
        else:
            return "Sin usuario asignado"


        # if obj.usuario and obj.usuario.sede:
        #     empresa_sede = obj.usuario.sede.empresasede_set.first()  # Obtener la primera relación
        #     return empresa_sede.empresa.nombre if empresa_sede else "Sin empresa"
        # return "Sin empresa"


class HistorialAsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAsignaciones
        fields = '__all__'
