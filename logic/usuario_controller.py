import bcrypt
from data.usuario_repository import findByEmail, save, findUsuarioAvailableByIdProyecto, existsByNombreAndApellido
from data.rol_repository import findAll as findRoles
from data.usuario_proyecto_repository import save as saveUsuarioProyecto
from data.usuario_proyecto_repository import findByIdProyecto
from utils.validators import get_password_crypt
from utils.exceptions.custom_exceptions import AccessDeniedException, AppException

def getUsuarioByEmailAndPassword(email, pass_texto_plano):
    usuario = findByEmail(email)
    if usuario is None:
        raise AccessDeniedException("Usuario o contraseña incorrectas!")
    pass_texto_plano = pass_texto_plano.encode()
    password_hasheada = usuario.password.encode()
    if bcrypt.checkpw(pass_texto_plano, password_hasheada):     # Validamos que las password coincidan
        return usuario
    else:
        raise AccessDeniedException("Usuario o contraseña incorrectas!")

def findAllRoles():
    roles = findRoles()
    return roles

def registrarNuevoUsuario(usuario):
    pre_validation(usuario, True)   # Validamos que el usuario no este registrado en la base de datos
    password_crypt = get_password_crypt(usuario.password)     # Generamos el hash del passoword del usuario
    usuario.password = password_crypt
    return save(usuario)

def getUsuariosDisponiblesParaProyecto(id_proyecto):
    return findUsuarioAvailableByIdProyecto(id_proyecto)

def asignarUsuarioProyecto(usuario_proyecto):
    return saveUsuarioProyecto(usuario_proyecto)

def getUsuariosByProyecto(id_proyecto):
    usuarios_proyectos = findByIdProyecto(id_proyecto)
    usuarios = []
    [usuarios.append(up.usuario) for up in usuarios_proyectos]
    return usuarios;

def pre_validation(usuario, is_create):
    valid: bool
    if is_create:
        valid = existsByNombreAndApellido(usuario.nombre, usuario.apellido)
        if valid:
            raise AppException("El usuario ya se encuentra registrado en la Base de datos!")
