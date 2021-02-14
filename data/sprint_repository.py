from conf.conexion import get_connection
from mysql.connector import Error
from data.proyecto_repository import findById as findProyecto
from models.models import Sprint
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad Sprint'''

def buildSprint(registro):
    estado = True if registro[5] == 1 else False
    # Obtenemos el proyecto por su id
    proyecto = findProyecto(registro[6])
    sprint = Sprint(registro[0], registro[1], registro[2], registro[3], registro[4], estado, proyecto)
    return sprint

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from sprints where id = %s"
            cursor.execute(select_query, (id,))
            return buildSprint(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByIdProyecto(id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from sprints where id_proyecto = %s"
            cursor.execute(select_query, (id_proyecto,))
            sprints, registros = [], cursor.fetchall()
            [sprints.append(buildSprint(registro)) for registro in registros]
            return sprints
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findByEstadoAndIdProyecto(estado, id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from sprints where estado = %s and id_proyecto = %s order by fecha_inicio desc limit 1"
            cursor.execute(select_query, (estado, id_proyecto))
            return buildSprint(cursor.fetchone())
    except (Exception, Error) as error:
        print("Error while getting data", error)

def save(sprint):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (sprint.nombre, sprint.fecha_inicio, sprint.fecha_fin, sprint.obs, sprint.estado,
                   sprint.proyecto.id)
            cursor.execute("insert into sprints(id, nombre, fecha_inicio, fecha_fin, obs, estado, id_proyecto) "
                           "values(default, %s, %s, %s, %s, %s, %s)", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def update(sprint):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (sprint.nombre, sprint.fecha_inicio, sprint.fecha_fin, sprint.obs,
                       sprint.estado, sprint.proyecto.id, sprint.id)
            cursor.execute("update sprints set nombre = %s, fecha_inicio = %s, fecha_fin = %s, obs = %s, estado = %s, "
                           "id_proyecto = %s where id = %s", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sprints WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)

def existSprintActivo(id_proyecto):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select count(id) from sprints where estado <> 1 and id_proyecto = %s"
            cursor.execute(select_query, (id_proyecto,))
            registro = cursor.fetchone()
            return True if registro[0] == 1 else False
    except (Exception, Error) as error:
        print("Error while getting data", error)
