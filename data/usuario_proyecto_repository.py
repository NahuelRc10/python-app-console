from conf.conexion import get_connection
from mysql.connector import Error
from data.usuario_repository import findById as findUsuario
from data.proyecto_repository import findById as findProyecto
from models.models import UsuarioProyecto
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad UsuarioProyecto'''

def buildUsuarioProyecto(self, registro):
    usuario = findUsuario(registro[1])   # Obtenemos el usuario por su id
    proyecto = findProyecto(registro[2])    # Obtenemos el proyecto por su id
    usuario_proyecto = UsuarioProyecto(registro[0], usuario, proyecto)
    return usuario_proyecto

def findAll():
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuarios_proyectos"
            cursor.execute(select_query)
            dto_list, registros = [], cursor.fetchall()
            [dto_list.append(buildUsuarioProyecto(registro)) for registro in registros]
            return dto_list
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuarios_proyectos where id = %s"
            cursor.execute(select_query, (id,))
            return buildUsuarioProyecto(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)


def findByIdUsuario(self, id_usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuarios_proyectos where id_usuario = %s"
            cursor.execute(select_query, (id_usuario,))
            dto_list, registros = [], cursor.fetchall()
            [dto_list.append(buildUsuarioProyecto(registro)) for registro in registros]
            return dto_list
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdProyecto(self, id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from usuarios_proyectos where id_proyecto = %s"
            cursor.execute(select_query, (id_proyecto,))
            dto_list, registros = [], cursor.fetchall()
            [dto_list.append(buildUsuarioProyecto(registro)) for registro in registros]
            return dto_list
    except (Exception, Error) as error:
        print("Error while getting data", error)

def save(usuario_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (usuario_proyecto.usuario.id, usuario_proyecto.proyecto.id)
            cursor.execute("insert into usuarios_proyectos(id, id_usuario, id_proyecto) "
                           "values(default, %s, %s)", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM usuarios_proyectos WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)
