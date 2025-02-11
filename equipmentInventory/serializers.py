from rest_framework import serializers
from .models import Empresa, Sede, EmpresaSede, Area, AreaSede, Departamento, Usuario, Estado, Equipo, HistorialAsignaciones

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


class AreaSedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaSede
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


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
