from data.proyecto_repository import save, findByIdLider, findByIdLiderAndLikeNombre, update, existsByNombre, findByIdUsuario, findByIdUsuarioAndLikeNombre
from utils.exceptions.custom_exceptions import AppException

def registrarNuevoProyecto(proyecto):
    pre_validation(proyecto, True)
    return save(proyecto)

def listarProyectosByModo(modo, usuario, nombre):
    if usuario.rol.nombre_rol == 'ADMIN':
        proyectos = findByIdLider(usuario.id) if modo == 1 else findByIdLiderAndLikeNombre(nombre, usuario.id)
    else:
        proyectos = findByIdUsuario(usuario.id) if modo == 1 else findByIdUsuarioAndLikeNombre(nombre, usuario.id)
    return proyectos

def actualizarProyecto(proyecto):
    return update(proyecto)

def listarProyectosByUsuario(id_usuario):
    return findByIdUsuario(id_usuario)

def pre_validation(proyecto, is_create):
    if is_create:
        valid = existsByNombre(proyecto.nombre)
        if valid:
            raise AppException("Ya existe un proyecto con ese nombre!")