from models.models import Rol
from conf.conexion import get_connection
from mysql.connector import Error
from contextlib import closing

''' Repository o DAO (Data Access Object) de la entidad Rol'''

def findAll():
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from roles"
            cursor.execute(select_query)
            roles, registros = [], cursor.fetchall()
            [roles.append(Rol(registro[0], registro[1])) for registro in registros]
            return roles
    except (Exception, Error) as error:
        print("Error while getting data", error)

def findById(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            select_query = "select * from roles where id = %s"
            cursor.execute(select_query, (id,))
            registro = cursor.fetchone()
            return Rol(registro[0], registro[1])
    except (Exception, Error) as error:
        print("Error while getting data", error)

def save(rol):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (rol.nombre_rol)
            cursor.execute("INSERT INTO roles(id, nombre_rol) VALUES(default, %s)", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while getting data", error)

def update(rol):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            valores = (rol.nombre_rol, rol.id)
            cursor.execute("UPDATE roles SET nombre_rol = %s WHERE id = %s", valores)
            return cursor.rowcount
    except (Exception, Error) as error:
        print("Error while getting data", error)

def delete(id):
    try:
        with closing(get_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM roles WHERE id = %s", (id,))
    except (Exception, Error) as error:
        print("Error while getting data", error)
