from data.requerimiento_repository import save, findWhenFechaFinIsNull, update, findByIdProyecto, findByIdSprintAndFechaFinIsNull, findByIdUsuario
from logic.sprint_controller import getSprintActivo

def registrarRequerimiento(req):
    return save(req)

def getRequerimientosPorTerminar(id_proyecto):
    return findWhenFechaFinIsNull(id_proyecto)

def asignarUsuario(req):
    return update(req)

def getRequerimientosByProyecto(id_proyecto):
    return findByIdProyecto(id_proyecto)

def actualizarSprintForRequerimientos(id_sprint):
    reqs = findByIdSprintAndFechaFinIsNull(id_sprint)
    if len(reqs) > 0:
        # Obtengo el sprint activo
        sprint_activo = getSprintActivo(reqs[0].get_proyecto().get_id())
        reqs = [r.set_sprint(sprint_activo) for r in reqs]
        # Actualizamos los requerimientos en la base de datos
        try:
            [update(reqs[i]) for i in range(0, len(reqs))]
            print("Requerimientos actualizados con exito!")
        except Exception as e:
            print(e)
    else:
        print("No hay requerimientos para actualizar")

def getRequerimientosByUsuario(id_usuario):
    return findByIdUsuario(id_usuario)