from io import open
from conf.conexion import get_connection
from mysql.connector import Error
from utils.email.email_service import enviar_email
import datetime

def generar_reporte_sprints(tipo_generacion, filtros):
    try:
        # Creamos la conexion a la base
        connection = get_connection()
        cursor = connection.cursor()
        usuario = filtros[2]
        valores = (filtros[0], filtros[1], usuario.get_id())
        select_query = ("select spr.nombre as nombreSprint, pro.nombre as nombreProyecto, count(req.id) as cantidadRequerimientos, concat(usu.apellido, ', ', usu.nombre) as nombreUsuario "
                        "from sprints spr "
                        "inner join proyectos pro on pro.id = spr.id_proyecto "
                        "left join requerimientos req on req.id_sprint = spr.id "
                        "inner join usuario usu on usu.id = pro.id_lider "
                        "where req.fecha_fin is not null "
                        "and req.fecha_fin between %s and %s "
                        "and pro.id_lider = %s "
                        "group by nombreSprint, nombreProyecto "
                        "order by nombreUsuario")
        # Ejecutamos la query para obtener los resultados del reporte
        cursor.execute(select_query, valores)
        registros = cursor.fetchall()
        connection.close()
        # Asignamos el nombre del archivo
        reporte_file_name = "reporte_print_" + str(datetime.datetime.now()) + ".txt"
        file = open('files/' + reporte_file_name, 'a')

        # Armamos la cabecera
        usuario_logueado = filtros[2]
        cabecera = "USUARIO LOGUEADO: " + usuario_logueado.get_apellido() + ", " + usuario_logueado.get_nombre()
        fecha_desde = filtros[0]
        fecha_hasta = filtros[1]
        cabecera = cabecera + "\n FECHA DESDE: " + fecha_desde + "\n FECHA HASTA: " + fecha_hasta + "\n"

        file.write(cabecera)

        if len(registros) > 0:
            columns = "Sprint \t\t" + "Proyecto \t\t" + "Cant. Requerimientos \t\t" + "Lider \n"
            file.write(columns)

            for registro in registros:
                detalle = registro[0] + "\t\t" + registro[1] + "\t\t" + registro[2] + "\t\t" + registro[3] + "\n"
                file.write(detalle)
        else:
            file.write("No hay datos!\n")
        # Cerramos el archivo
        file.close()

        if tipo_generacion == 1:
            # Implica generacion en la carpeta directory del proyecto
            return file
        else:
            # Implica ademas su envio por mail
            asunto = "Envio de reporte por email"
            enviar_email(usuario_logueado.get_email(), asunto, "", file)
    except (Exception, Error) as error:
        print("Error while getting data", error)
