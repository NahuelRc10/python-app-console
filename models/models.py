from dataclasses import dataclass
import datetime

@dataclass
class Rol:      # ENTITY ROL
    id: int
    nombre_rol: str

@dataclass
class Usuario:      # ENTITY USUARIO
    id: int
    nombre: str
    apellido: str
    genero: str
    email: str
    password: str
    telefono: str
    rol: Rol

@dataclass
class Proyecto:     # ENTITY PROYECTO
    id: int
    nombre: str
    descripcion: str
    cantidad_integrantes: int
    total_precio: float
    total_horas: int
    lider: Usuario

@dataclass
class UsuarioProyecto:      # ENTITY USUARIOPROYECTO
    id: int
    usuario: Usuario
    proyecto: Proyecto

@dataclass
class Sprint:       # ENTIDAD SPRINT
    id: int
    nombre: str
    fecha_inicio: datetime.datetime
    fecha_fin: datetime.datetime
    obs: str
    estado: bool
    proyecto: Proyecto

@dataclass
class Requerimiento:        # ENTIDAD REQUERIMIENTO
    id: int
    nombre: str
    cant_hora: int
    fecha_inicio: datetime.datetime
    fecha_fin: datetime.datetime
    descripcion: str
    observacion: str
    sprint: Sprint
    usuario: Usuario
    proyecto: Proyecto