from models.models import Proyecto
from conf.conexion import get_connection
from mysql.connector import Error
from data.usuario_repository import findById as findUsuario
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad Proyecto'''

def buildProyecto(registro):
    lider = findUsuario(registro[6])    # Buscamos al lider de proyecto por su id
    proyecto = Proyecto(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], lider)
    return proyecto

def findAll():
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from proyectos"
            cursor.execute(select_query)
            proyectos, registros = [], cursor.fetchall()
        [proyectos.append(buildProyecto(registro)) for registro in registros]
        return proyectos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdUsuario(id_usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = '''select pro.* 
                              from proyectos pro
                              inner join usuarios_proyectos up on up.id_proyecto = pro.id
                              where up.id_usuario = %s '''
            cursor.execute(select_query, (id_usuario,))
            proyectos, registros = [], cursor.fetchall()
        [proyectos.append(buildProyecto(registro)) for registro in registros]
        return proyectos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdUsuarioAndLikeNombre(nombre, id_usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            param = '{}%'.format(nombre)
            select_query = '''select pro.* 
                              from proyectos pro
                              inner join usuarios_proyectos up on up.id_proyecto = pro.id
                              where pro.nombre like %s and up.id_usuario = %s '''
            cursor.execute(select_query, (param, id_usuario))
            proyectos, registros = [], cursor.fetchall()
        [proyectos.append(buildProyecto(registro)) for registro in registros]
        return proyectos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from proyectos where id = %s"
            cursor.execute(select_query, (id,))
            return buildProyecto(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def existsByNombre(nombre):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select count(id) from proyectos where nombre = %s"
            cursor.execute(select_query, (nombre,))
            registro = cursor.fetchone()
            return True if registro[0] == 1 else False
    except (Exception, Error) as error:
        print("Error while getting data", error)

def save(proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (proyecto.nombre, proyecto.descripcion, proyecto.cantidad_integrantes, proyecto.total_precio,
                       proyecto.total_horas, proyecto.lider.id)
            cursor.execute("insert into proyectos(id, nombre, descripcion, cantidad_integrantes, total_precio, total_horas, id_lider) "
                           "values(default, %s, %s, %s, %s, %s, %s)", valores)
        return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def update(proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (proyecto.nombre, proyecto.descripcion, proyecto.cantidad_integrantes, proyecto.total_precio,
                       proyecto.total_horas, proyecto.lider.id, proyecto.id)
            cursor.execute("update proyectos set nombre = %s, descripcion = %s, cantidad_integrantes = %s, total_precio = %s, total_horas = %s, "
                "id_lider = %s where id = %s", valores)
        return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM proyectos WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)