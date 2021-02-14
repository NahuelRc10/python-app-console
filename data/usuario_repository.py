from models.models import Usuario
from conf.conexion import get_connection
from mysql.connector import Error
from data.rol_repository import findById as findRol
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad Usuario'''

def buildUsuario(registro):
    rol = findRol(registro[7])      # Buscamos el rol del usuario por su id_rol
    usuario = Usuario(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], rol)
    return usuario

def findAll():
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuario"
            cursor.execute(select_query)
            usuarios, registros = [], cursor.fetchall()
            [usuarios.append(buildUsuario(registro)) for registro in registros]
            return usuarios
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuario where id = %s"
            cursor.execute(select_query, (id,))
            return buildUsuario(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByEmail(email):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuario where email = %s"
            cursor.execute(select_query, (email,))
            return buildUsuario(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findUsuarioAvailableByIdProyecto(id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = ("select * from usuario us "
                            "where us.id not in (select up.id_usuario "
                            "from usuarios_proyectos up "
                            "inner join usuario u on u.id = up.id_usuario "
                            "inner join roles r on r.id = u.id_rol "
                            "where up.id_proyecto = %s and r.nombre_rol <> 'ADMIN') and us.id_rol <> 1")
            cursor.execute(select_query, (id_proyecto,))
            usuarios, registros = [], cursor.fetchall()
            [usuarios.append(buildUsuario(registro)) for registro in registros]
            return usuarios
    except (Exception, Error) as error:
        print("Error while getting data", error)

def existsByNombreAndApellido(nombre, apellido):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select count(id) from usuario where nombre = %s and apellido = %s"
            cursor.execute(select_query, (nombre, apellido))
            registro = cursor.fetchone()
            return True if registro[0] == 1 else False
    except (Exception, Error) as error:
        print("Error while getting data", error)

def save(usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (usuario.nombre, usuario.apellido, usuario.genero, usuario.email,
                       usuario.password, usuario.telefono, usuario.rol.id)
            cursor.execute("insert into usuario(id, nombre, apellido, genero, email, password, telefono, id_rol) "
                           "values(default, %s, %s, %s, %s, %s, %s, %s)", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def update(usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (usuario.nombre, usuario.apellido, usuario.genero, usuario.email,
                       usuario.password, usuario.telefono, usuario.rol.id, usuario.id)
            cursor.execute("update usuario set nombre = %s, apellido = %s, genero = %s, email = %s, password = %s, "
                           "telefono = %s, id_rol = %s where id = %s", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)
