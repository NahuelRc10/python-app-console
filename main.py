import datetime
from models.models import Usuario, Proyecto, UsuarioProyecto, Sprint, Requerimiento
from utils.validators import valida_email, valid_input_string, valid_input_number, valid_input_float, valid_opt_between_ranges, valida_input_date, valida_input_date_hasta
from utils.exceptions.custom_exceptions import AccessDeniedException, AppException
from logic.usuario_controller import getUsuarioByEmailAndPassword, findAllRoles, registrarNuevoUsuario, getUsuariosDisponiblesParaProyecto, asignarUsuarioProyecto, getUsuariosByProyecto
from logic.proyecto_controller import registrarNuevoProyecto, listarProyectosByModo, actualizarProyecto, listarProyectosByUsuario
from logic.sprint_controller import validIfExistsSprintActivoProyecto, registrarSprint, listarSprintsByProyecto, getSprintActivo, cerrarSprint
from logic.requerimiento_controller import registrarRequerimiento, getRequerimientosPorTerminar, asignarUsuario, getRequerimientosByProyecto, actualizarSprintForRequerimientos, getRequerimientosByUsuario
from logic.reporte_controller import generar_reporte_sprints

# VARIABLES GLOBALES DE LA APP
usuario_login: Usuario
PASSWORD_DEFAULT = "abc123456"
CANTIDAD_INTEGRANTES_DEFAULT = 1

def welcome():
    print(" ---------------------------------------------------------------------------------------")
    print("|                              BIENVENIDO A LA APLICACION                               |")
    print(" ---------------------------------------------------------------------------------------")
    global usuario_login
    usuario_login = login()
    rol = usuario_login.rol
    if rol.nombre_rol == 'ADMIN' or rol.nombre_rol == 'LIDER_AREA':
        print("\tBIENVENIDO " + usuario_login.nombre + ", " + usuario_login.apellido)
        show_menu_admin()


    elif rol.nombre_rol == 'DEVELOPER' or rol.nombre_rol == 'DEV_OPS' \
            or rol.nombre_rol == 'ADM_BASE_DATOS' or rol.nombre_rol == 'LIDER_TECNICO':
        a = 2
    else:
        # ROL ---> ANALISTA_FUNCIONAL
        show_menu_analista()

def login():
    login_flag = False
    while login_flag is False:
        email_flag = False
        while email_flag is False:
            email = input("\t-Ingresa email: \n")
            email_flag = valida_email(email)
        password = input("\t-Ingresa password: \n")
        try:
            usuario = getUsuarioByEmailAndPassword(email, password)
            if usuario is not None:
                login_flag = True
                email_flag = False
        except AccessDeniedException as e:
            print(e.message)
    return usuario

def show_menu_admin():
    print("\t1- Registrar nuevo usuario")
    print("\t2- Proyecto")
    print("\t3- Reportes")
    print("\t0- SALIR")
    option = int(input("\t- Ingresa una opcion: "))
    while option != 0:
        if option == 1:
            carga_datos_usuario()
        elif option == 2:
            # Submenu
            print("\t1- Crear Proyecto")
            print("\t2- Editar Proyecto existente")
            print("\t3- Asignar usuario a Proyecto")
            print("\t4- Crear nuevo Sprint")
            print("\t5- Listar Sprints")
            print("\t6- Agregar requerimiento")
            print("\t7- Asignar requerimiento")
            print("\t8- Listar requerimientos")
            print("\t0- Volver")
            flag = False
            while flag is False:
                option_proy = int(input("\t- Ingresa una opcion del menu de Proyectos: "))
                flag = True if option_proy >= 0 & option_proy < 6 else False
            exec_option_menu_proyecto(option_proy)
        elif option == 3:
            ejecutar_reporte()
        option = int(input("\t- Ingresa una opcion: "))

def show_menu_analista():
    print("\t1- Agregar requerimiento")
    print("\t2- Editar requerimiento")
    print("\t3- Listar requerimientos")
    print("\t4- Ver mis proyectos")
    print("\t5- Ver mis requerimientos")
    print("\t6- Asignar requerimiento")
    print("\t0- SALIR")
    option = int(input("\t- Ingresa una opcion: "))
    while option != 0:
        if option == 1:
            cargar_datos_requerimiento()
        if option == 2:
            print("NO DESARROLLADO")
        if option == 3:
            listar_requerimientos()
        if option == 4:
            ver_mis_proyectos()
        if option == 5:
            ver_requerimientos()
        if option == 6:
            asignar_requerimiento()

def show_menu_common():
    print("\t1- Editar requerimiento")
    print("\t2- Ver mis proyectos")
    print("\t3- Ver mis requerimientos")
    print("\t0- SALIR")
    option = int(input("\t- Ingresa una opcion: "))
    while option != 0:
        if option == 1:
            print("NO DESARROLLADO")
        if option == 2:
            ver_mis_proyectos()
        if option == 3:
            ver_requerimientos()

'''
Metodo para realizar las acciones del sub menu de proyectos
'''
def exec_option_menu_proyecto(option_proy):
    if option_proy == 1:
        carga_datos_proyecto()
    if option_proy == 2:
        editar_proyecto()
    if option_proy == 3:
        asignar_usuario()
    if option_proy == 4:
        carga_datos_sprint()
    if option_proy == 5:
        listar_sprints()
    if option_proy == 6:
        cargar_datos_requerimiento()
    if option_proy == 7:
        asignar_requerimiento()
    if option_proy == 8:
        listar_requerimientos()

def ver_mis_proyectos():
    proyectos = listarProyectosByUsuario(usuario_login.id())
    if len(proyectos) > 0:
        [print(str(i) + " - " + proyectos[i].nombre) for i in range(0, len(proyectos))]

def ver_requerimientos():
    reqs = getRequerimientosByUsuario(usuario_login.id())
    if len(reqs) > 0:
        [r.__str__() for r in reqs]

def get_validated_imput(message, error_message, validators):
    while True:
        cadena = input("\t" + message)
        if all(validator(cadena) for validator in validators):
            return cadena
        print(error_message)

def get_validated_input_float(mensaje1, error_message):
    valor = input("\t" + mensaje1)
    while True:
        try:
            valor = float(valor)
        except ValueError:
            print("\t" + error_message)
            continue
        if valor < 0:
            print("\t Valor no valido")
        else:
            break
    return valor

def carga_datos_usuario():
    print("\t FORMULARIO REGISTRO USUARIO")
    usuario = Usuario(None, None, None, None, None, None, None, None)
    nombre = apellido = genero = email = password = telefono = ""
    nombre = get_validated_imput("- Ingresa el nombre del usuario: ", "Este campo no puede contener numeros", [str.isalpha])
    apellido = get_validated_imput("- Ingresa el apellido del usuario: ", "Este campo no puede contener numeros", [str.isalpha])
    flag = False
    while flag is False:
        genero = input("\t- Ingresa el sexo del usuario (M-> Masculino / F-> Femenino): ")
        flag = True if genero == 'M' or genero == 'F' else False

    email = get_validated_imput("- Ingresa el email del usuario: ", "Email no valido", [valida_email])

    # Al momento del registro se establece una contraseña por default, el usuario despues podra modificar dicha contraseña
    password = PASSWORD_DEFAULT
    telefono = valid_input_number("- Ingresa telefono del usuario: ", "Este campo no puede contener letras")

    # Listamos los roles
    roles_list = findAllRoles()
    i = 1
    for rol in roles_list:
        print("\t" + str(i) + "-" + rol.nombre_rol)
        i += 1
    print("\t- Elije un rol: ")
    rol_option = valid_opt_between_ranges(1, len(roles_list))

    # Disminuimos en uno la opcion ingresada por el usuario
    rol_usuario = roles_list[rol_option - 1]

    # Seteamos los valores de las entradas en el objeto de tipo Usuario
    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.genero = genero
    usuario.email = email
    usuario.password = password
    usuario.telefono = telefono
    usuario.rol = rol_usuario
    print(usuario.__str__())
    try:
        usuario_db = registrarNuevoUsuario(usuario)
        print("Usuario registrado con exito" if usuario_db == 1 else "Ocurrio un error en el proceso de registracion!")
    except AppException as e:
        print(e.message())

def carga_datos_proyecto():
    print("\t FORMULARIO REGISTRO PROYECTO")
    precio_x_hora = total_horas = 0
    proyecto = Proyecto(None, None, None, None, None, None, None)
    flag = False
    nombre = input("\t- Ingresa el nombre del proyecto: ")
    descripcion = input("\t- Ingresa una breve descripcion del proyecto: ")
    cant_horas = int(get_validated_imput("- Ingresa la cantidad de horas estimadas del proyecto: ", "Este campo no puede contener letras", [str.isdigit]))
    precio_x_hora = float(get_validated_imput("- Ingresa el precio por hora: ", "Precio no valido", [valid_input_float]))
    total_precio = cant_horas * precio_x_hora
    cant_integrantes = CANTIDAD_INTEGRANTES_DEFAULT
    lider_proyecto = usuario_login

    # Seteamos los valores en el objeto
    proyecto.nombre = nombre
    proyecto.descripcion = descripcion
    proyecto.cantidad_integrantes = cant_integrantes
    proyecto.total_horas = cant_horas
    proyecto.total_precio = total_precio
    proyecto.lider = lider_proyecto
    try:
        proyecto_db = registrarNuevoProyecto(proyecto)
        print("Proyecto registrado con exito!" if proyecto_db == 1 else "Ocurrio un error en la registracion del proyecto")
    except AppException as e:
        print(e.message())

def editar_proyecto():
    print("\t EDICION DE PROYECTOS")
    proyecto_seleccionado = seleccionar_proyecto()
    if proyecto_seleccionado is not None:
        cant_horas = precio_x_hora = 0
        descripcion = input("\t- Ingresa la descripcion del proyecto: ")
        cant_horas = valid_input_number("- Ingresa la cantidad de horas estimadas del proyecto: ", "Este campo no puede contener letras")
        precio_x_hora = valid_input_float("- Ingresa el precio por hora: ", "Precio no valido")

        total_precio = proyecto_seleccionado.total_precio + cant_horas * precio_x_hora
        proyecto_seleccionado.total_horas = proyecto_seleccionado.total_horas() + cant_horas
        proyecto_seleccionado.total_precio = total_precio
        proyecto_seleccionado.descripcion = descripcion
        actualiza = actualizarProyecto(proyecto_seleccionado)
        print("Proyecto actualizado correctamente!" if actualiza > 0 else "Ocurrio un error mientras se actualizaba el proyecto!")

def asignar_usuario():
    print("\t ASIGNACION A PROYECTOS")
    proyecto_seleccionado = seleccionar_proyecto()
    if proyecto_seleccionado is not None:
        flag_asignar = True
        while flag_asignar is True:
            print("\t Selecciona los usuarios")
            usuarios_av = getUsuariosDisponiblesParaProyecto(proyecto_seleccionado.id)
            [print("\t" + str(i) + usuarios_av[i].__repr__) for i in range(0, len(usuarios_av))]
            if len(usuarios_av) > 0:
                opt = valid_opt_between_ranges(0, len(usuarios_av))
                usuario_seleccionado = usuarios_av[opt]
                usuario_proyecto = UsuarioProyecto(None, usuario_seleccionado, proyecto_seleccionado)

                try:
                    rta = asignarUsuarioProyecto(usuario_proyecto)
                    print("Usuario asignado correctamente al Proyecto!" if rta == 1 else "Ocurrio un error en el proceso de asignacion!")
                except AppException as e:
                    print(e.message())
                a = int(input("\t Desea asignar otro usuario? 1.Si | 2.No: "))
                flag_asignar = True if a == 1 else False
            else:
                flag_asignar = False
                print("\t No hay usuarios disponibles para asignar al proyecto")

def carga_datos_sprint(proyecto = None):
    print("\t Seleccionar proyecto")
    proyecto = seleccionar_proyecto() if proyecto is None else proyecto
    exist_sprint_activo = validIfExistsSprintActivoProyecto(proyecto.id)
    if exist_sprint_activo:
        print("\tYa existe un sprint activo para el proyecto seleccionado")
        print("\tPrimero cierre el sprint activo")
        cerrar = int(input("\t Desea cerrar el sprint? 1.Si | 2.No"))
        if cerrar == 1:
            cerrar_sprint(proyecto)
    else:
        print("\t FORMULARIO NUEVO SPRINT")
        nombre = input("\t- Ingresa el nombre del sprint: ")
        fecha_inicio = datetime.datetime.now()
        cant_dias_sprint = valid_input_number("- Ingresa la cantidad de dias que dura el sprint: ", "Este campo no puede contener letras")
        fecha_fin = fecha_inicio + datetime.timedelta(days=cant_dias_sprint)
        observaciones = input("\t- Ingresa observaciones: ")

        try:
            # Seteamos los valores en el objeto
            sprint = Sprint(None, None, None, None, None, None, None)
            sprint.nombre = nombre
            sprint.fecha_inicio = fecha_inicio
            sprint.fecha_fin = fecha_fin
            sprint.obs = observaciones
            sprint.estado = False
            sprint.proyecto = proyecto
            row = registrarSprint(sprint)
            print("Sprint registrado con exito!" if row == 1 else "Ocurrio un error!")
        except Exception as e:
            print(e)

def cerrar_sprint(proyecto):
    sprint_activo = getSprintActivo(proyecto.id)
    # Cerramos el sprint cambiando el estado a true
    sprint_activo.estado = True
    rta = cerrarSprint(sprint_activo)
    print("Sprint cerrado correctamente!" if rta == 1 else "No se pudo cerrar el Sprint")
    if rta == 1:
        print("\t Carga un nuevo Sprint para el proyecto")
        carga_datos_sprint(proyecto)
        # Actualizamos el sprint de los requerimientos que no esten finalizados
        actualizarSprintForRequerimientos(sprint_activo.id)

def listar_sprints():
    proyecto = seleccionar_proyecto()
    print("\t LISTADO DE SPRINTS DEL PROYECTO " + proyecto.nombre.upper())
    sprints = listarSprintsByProyecto(proyecto.id)
    print("\t Nombre Sprint \t\t Fecha Inicio \t\t Fecha Fin \t\t Estado \t\t Proyecto")
    [print("\t " + s.nombre + "\t\t" + str(s.fecha_inicio) + "\t\t" + str(s.fecha_fin) + "\t\t" + str(s.estado) + "\t\t" + s.proyecto.nombre) for s in sprints]

def cargar_datos_requerimiento():
    proyecto = seleccionar_proyecto()
    sprint_activo = getSprintActivo(proyecto.id)
    if sprint_activo is not None:
        print("\t FORMULARIO ALTA REQUERIMIENTO")
        nombre = input("\t- Ingresa el nombre del requerimiento: ")
        cant_horas= valid_input_number("- Ingresa la cantidad de horas estimadas del requerimiento: ", "Este campo no puede contener letras")
        descripcion = input("\t- Ingresa descripcion del requerimiento: ")
        observacion = input("\t- Ingresa observacion del requerimietno: ")

        # Seteamos los valores al objeto
        req = Requerimiento(None, None, None, None, None, None, None, None, None, None)
        req.nombre = nombre
        req.cant_hora = cant_horas
        req.descripcion = descripcion
        req.observacion = observacion
        req.sprint = sprint_activo
        req.proyecto = proyecto
        rta = registrarRequerimiento(req)
        print("Requerimiento registrado con exito!" if rta == 1 else "Ocurrio un error en la registracion")
    else:
        print("No existe un sprint activo para el proyecto seleccionado!")

def asignar_requerimiento():
    proyecto = seleccionar_proyecto()
    print("\t REQUERIMIENTOS POR ASIGNAR")
    # Listamos los requerimientos que aun no han sido asignados
    reqs = getRequerimientosPorTerminar(proyecto.id)
    if len(reqs) > 0:
        print("\t Nombre Requerimiento \t\t Fecha Inicio \t\t Fecha Fin \t\t Sprint \t\t Proyecto")
        [print("\t " + reqs[i].nombre + "\t\t" + str(reqs[i].fecha_inicio) + "\t\t" + str(reqs[i].fecha_fin) + "\t\t" + reqs[i].sprint.nombre +
               "\t\t" + reqs[i].proyecto.nombre) for i in range(0, len(reqs))]
        print("\t Seleccione un requerimiento")
        opt = valid_opt_between_ranges(0, len(reqs))
        req_seleccionado = reqs[opt]
        # Listamos los usuarios del curso
        usuarios = getUsuariosByProyecto(proyecto.id)
        if len(usuarios) > 0:
            print("\t USUARIOS MIEMBROS DEL EQUIPO DEL PROYECTO " + proyecto.nombre.upper())
            [print("\t" + str(i) + " - " + usuarios[i].apellido + ", " + usuarios[i].nombre  + "\t Rol:" + usuarios[i].rol.nombre_rol) for i in range(0, len(usuarios))]
            print("\t Seleccione un usuario")
            opt_usuario = valid_opt_between_ranges(0, len(usuarios))
            usuario_seleccionado = usuarios[opt_usuario]
            req_seleccionado.usuario = usuario_seleccionado
            rta = asignarUsuario(req_seleccionado)
            print("Requerimiento asignado correctamente!" if rta == 1 else "Ocurrio un error!")
        else:
            print("\t No existen usuarios asignados al proyecto")
            asignar_usuario()
    else:
        print("\t No hay requerimientos sin asignar!")

def listar_requerimientos():
    proyecto = seleccionar_proyecto()
    print("\t LISTADO DE REQUERIMIENTO DEL PROYECTO " + proyecto.nombre.upper())
    reqs = getRequerimientosByProyecto(proyecto.id)
    print("\t Nombre Req. \t\t Fecha Inicio \t\t Fecha Fin \t\t Usuario \t\t Proyecto \t\t Sprint")
    [print("\t " + r.nombre + "\t\t" + str(r.fecha_inicio) + "\t\t" + str(r.fecha_fin) + "\t\t" + str(r.usuario.apellido) + "\t\t" + r.proyecto.nombre + "\t\t" + r.sprint.nombre)
     for r in reqs]

def seleccionar_proyecto():
    print("\t Ingrese como desea buscar el proyecto a editar")
    print("\t1- Por ID\n\t2- Por nombre")
    modo = valid_opt_between_ranges(1, 2)
    nombre = ""
    if modo == 2:
        nombre = input("\t- Ingresa nombre de los proyectos a buscar")

    proyectos = listarProyectosByModo(modo, usuario_login, nombre)
    [print(str(i) + " - " + proyectos[i].nombre) for i in range(0, len(proyectos))]
    print("\t- Selecciona un proyecto")
    if len(proyectos) > 0:
        opt = valid_opt_between_ranges(0, len(proyectos))
        proyecto_seleccionado = proyectos[opt]
        return proyecto_seleccionado
    else:
        print("No se encontraron proyectos segun los filtros ingresados!")
        return None

def ejecutar_reporte():
    '''
        Este reporte filtrara los datos por 3 filtros: Fecha desde, fecha hasta y usuario logueado
    '''
    filtros = []
    fecha_desde = valida_input_date("Ingresa fecha desde en el formato YYYY-MM-DD: ")
    fecha_hasta = valida_input_date_hasta("Ingresa fecha hasta en el formato YYYY-MM-DD: ", fecha_desde)
    filtros.append(str(fecha_desde))
    filtros.append(str(fecha_hasta))
    filtros.append(usuario_login)

    print("\t\t TIPO GENERACION DEL REPORTE")
    print("\t\t1- Directorio del proyecto")
    print("\t\t2- Enviar al email")
    tipo_generacion = valid_opt_between_ranges(1, 2)

    reporte = generar_reporte_sprints(tipo_generacion, filtros)



welcome()
