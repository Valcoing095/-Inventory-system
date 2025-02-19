from django.db import models

# ============================== #
#        MODELO DE EMPRESA       #
# ============================== #

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre


# ============================== #
#          MODELO SEDE           #
# ============================== #

class Sede(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"

    def __str__(self):
        return self.nombre


# ============================================ #
#     RELACIÓN N:M ENTRE EMPRESA Y SEDE        #
# ============================================ #

class EmpresaSede(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE,null=True)

    class Meta:
        unique_together = ('empresa', 'sede')
        verbose_name = "Empresa - Sede"
        verbose_name_plural = "Empresas - Sedes"

    def __str__(self):
        return f"{self.empresa.nombre} - {self.sede.nombre}"


# ============================== #
#          MODELO ÁREA           #
# ============================== #

class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.nombre


# ============================== #
#       MODELO DEPARTAMENTO      #
# ============================== #

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    area = models.ForeignKey(Area, on_delete = models.CASCADE,null=True)
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre
# ============================== #
#         MODELO USUARIO         #
# ============================== #

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    username_ad = models.CharField(max_length=100)  # Usuario en Active Directory
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    empresa_sede = models.ForeignKey(EmpresaSede, on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} ({self.username_ad}) "

# ============================== #
#         MODELO ESTADO          #
# ============================== #

class Estado(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('En mantenimiento', 'En mantenimiento'),
        ('Dado de baja', 'Dado de baja'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS, unique=True)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    def __str__(self):
        return self.estado


# ============================== #
#         MODELO EQUIPO          #
# ============================== #

class Equipo(models.Model):
    serial = models.CharField(max_length=50, unique=True)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    procesador = models.CharField(max_length=100)
    disco_duro = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100, null=True, blank=True)
    costo_unitario = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return f"{self.modelo} ({self.serial})"


# ======================================== #
#      MODELO HISTORIAL DE ASIGNACIONES    #
# ======================================== #

class HistorialAsignaciones(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Historial de Asignación"
        verbose_name_plural = "Historial de Asignaciones"

    def __str__(self):
        return f"{self.equipo.serial} asignado a {self.usuario.nombre} el {self.fecha_asignacion}"
