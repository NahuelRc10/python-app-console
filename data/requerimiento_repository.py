from mysql.connector import Error
from data.proyecto_repository import findById as findProyecto
from data.sprint_repository import findById as findSprint
from data.usuario_repository import findById as findUsuario
from models.models import Requerimiento
from conf.conexion import get_connection
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad Requerimiento'''

def builRequerimiento(registro):
    sprint = findSprint(registro[7])     # Obtenemos el sprint en base a su id
    usuario = findUsuario(registro[8]) if registro[8] is not None else None     # Obtenemos el usuario en base a su id
    proyecto = findProyecto(registro[9])       # Obtenemos el proyecto en base a su id
    requerimiento = Requerimiento(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6],
                                  sprint, usuario, proyecto)
    return requerimiento

def save(req):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (req.nombre, req.cant_hora, req.fecha_inicio, req.fecha_fin,
                       req.descripcion, req.observacion, req.sprint.id, req.proyecto.id)
            cursor.execute("insert into requerimientos(id, nombre, cant_horas, fecha_inicio, fecha_fin, descripcion, observacion, id_sprint, id_usuario, id_proyecto) "
            "values(default, %s, %s, %s, %s, %s, %s, %s, null, %s)", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findAll():
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos"
            cursor.execute(select_query)
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where id = %s"
            cursor.execute(select_query, (id,))
            return builRequerimiento(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdProyecto(id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where id_proyecto = %s"
            cursor.execute(select_query, (id_proyecto,))
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdSprintAndFechaFinIsNull(id_sprint):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where id_sprint = %s and fecha_fin is null"
            cursor.execute(select_query, (id_sprint,))
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdUsuario(id_usuario):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where id_usuario = %s"
            cursor.execute(select_query, (id_usuario,))
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByUsuarioAndProyecto(id_usuario, id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where id_usuario = %s and id_proyecto = %s"
            cursor.execute(select_query, (id_usuario, id_proyecto))
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findWhenFechaFinIsNull(id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from requerimientos where fecha_fin is null and id_usuario is null and id_proyecto = %s"
            cursor.execute(select_query, (id_proyecto,))
            requerimientos, registros = [], cursor.fetchall()
            [requerimientos.append(builRequerimiento(registro)) for registro in registros]
            return requerimientos
    except (Exception, Error) as error:
        print("Error while getting data", error)

def update(req):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (req.nombre, req.cant_hora, req.fecha_inicio, req.fecha_fin, req.descripcion,
                req.observacion,req.sprint.id, req.usuario.id, req.proyecto.id, req.id)
            cursor.execute("update requerimientos set nombre = %s, cant_horas = %s, fecha_inicio = %s, fecha_fin = %s, descripcion = %s, observacion = %s, "
                       "id_sprint = %s, id_usuario = %s, id_proyecto = %s where id = %s", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM requerimientos WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)

