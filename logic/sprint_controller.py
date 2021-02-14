from data.sprint_repository import existSprintActivo, save, findByIdProyecto, findByEstadoAndIdProyecto, update

def validIfExistsSprintActivoProyecto(id_proyecto):
    return existSprintActivo(id_proyecto)

def registrarSprint(sprint):
    return save(sprint)

def listarSprintsByProyecto(id_proyecto):
    return findByIdProyecto(id_proyecto)

def getSprintActivo(id_proyecto):
    return findByEstadoAndIdProyecto(False, id_proyecto)

def cerrarSprint(sprint):
    return update(sprint)