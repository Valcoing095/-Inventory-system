from rest_framework import serializers
from .models import Empresa, Sede, EmpresaSede, Area, Departamento, Usuario, Estado, Equipo, HistorialAsignaciones

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'

class EmpresaSedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaSede
        fields = '__all__'

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
    id_area = serializers.IntegerField(source="departamento.area.id", read_only=True)
    sede_nombre = serializers.IntegerField(source="sede.nombre", read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id", "nombre", "cargo", "correo", "username_ad", 
            "departamento","sede",  # Campo escribible
            "departamento_nombre", "area", "id_area", "sede","sede_nombre"  # Campos de solo lectura
        ]
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Equipo
        fields = '__all__'

class HistorialAsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAsignaciones
        fields = '__all__'
