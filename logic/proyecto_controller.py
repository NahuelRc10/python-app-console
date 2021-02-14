from data.proyecto_repository import save, findByIdUsuario, findByIdUsuarioAndLikeNombre, update, existsByNombre
from utils.exceptions.custom_exceptions import AppException

def registrarNuevoProyecto(proyecto):
    pre_validation(proyecto, True)
    return save(proyecto)

def listarProyectosByModo(modo, usuario, nombre):
    if modo == 1:
        proyectos = findByIdUsuario(usuario.id)   # Por lider
    else:
        proyectos = findByIdUsuarioAndLikeNombre(nombre, usuario.id)      # Por nombre y id_lider
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