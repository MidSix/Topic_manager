import json
import os
from datetime import datetime
#-----------------------------------------------------------Funciones usadas para "crear materia"---------------------------------------------------------------------------------
ARCHIVO_DATOS = "datos.json"
TEMP = "temp.json" #En temp.json están las materias que tienen sesiones abiertas.
def cargar_materias():
    if not os.path.exists(ARCHIVO_DATOS) or os.path.getsize(ARCHIVO_DATOS) == 0:    #Manejo de errores:
        #Si el archivo no existe en el cwd(current work directory) entrará en el condicional, si existe pero está vacío completamente también entrará en el condicional
        #tras entrar creará ARCHIVO_DATOS, para el caso por default: datos.json con y le escribirá un diccionario vacío porque si se intenta cargar con load 
        #un .json vacío sin siquiera un {} dará error porque el método espera que al menos tenga un diccionario vacío para cargar datos. Si existe pero está vacío
        #entonces lógicamente no creará el archivo sino que solo entrará en él y escribirá un {} para que funcione load después.
        with open(ARCHIVO_DATOS, "w") as file:
            json.dump({}, file)

    with open(ARCHIVO_DATOS, "r") as archivo:
        return json.load(archivo)

def guardar_materia(datos):
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def new_topic(nombre: str, objetivo:int):
    datos = cargar_materias()

    nueva_materia = {
        "objetivo_horas": objetivo,
        "tiempo_acumulado": 0.0,
        "sesiones": []
    }

    datos[nombre] = nueva_materia   #Estamos añadiendo un par clave-valor al diccionario.
    guardar_materia(datos)    #Guardamos en el Json el diccionario con el nuevo par clave-valor que acabamos de crear.
    return datos

def eliminiar_materia(nombre: str):
    datos = cargar_materias()
    if nombre in datos:
        del datos[nombre]
        guardar_materia(datos)
        return datos
    else:
        return None
#--------------------------------------------------------Funciones usadas para iniciar una sesión-----------------------------------------------------------------------------------------------------------------

def cargar_sesiones():
    if not os.path.exists(TEMP) or os.path.getsize(TEMP) == 0:
        with open(TEMP, "w") as temp:
            json.dump({}, temp)

    with open(TEMP, "r") as tmp:
        return json.load(tmp)

def guardar_sesion(datos):
    with open(TEMP, "w") as tmp:
        json.dump(datos, tmp)

def iniciar_sesion(materia: str):
    temp = cargar_sesiones()
    if not materia in temp:
        temp[materia] = datetime.now().isoformat()
        guardar_sesion(temp)
        return temp
    else:
        return 1
#-----------------------------------------------------------------Funciones usadas para terminar una sesión------------------------------------------------------------------
def terminar_sesion(materia: str):
    datos = cargar_materias()
    sesiones = cargar_sesiones()
    momento_final = datetime.now() #Aqui no usamos el isoformat method, entonces al objeto en memoria que apunta el identificador momento_final es tipo datetime y no string.
    #---Para hacer operaciones como restas, sumas y demas entre fechas tenemos que tener los dos objetos tipo datetime, porque esos objetos tendran ahi sus metodos para 
    #Manejar estas operaciones.

    momento_inicial = sesiones[materia] #Lo carga desde el diccionario cargado a este modulo  de temp.Json, por lo tanto es de tipo string. Hemos de pasarlo a datetime.
    momento_inicial = datetime.fromisoformat(momento_inicial)
    duracion = (momento_final - momento_inicial).total_seconds() / 3600 # en horas.
    #Actualizacion del diccionario:
    datos[materia]["tiempo_acumulado"] += duracion
    datos[materia]["sesiones"].append({
        "inicio": momento_inicial.isoformat(),
        "fin"   : momento_final.isoformat()
    })
    del(sesiones[materia])
    #Con esto sobreescribimos datos. / si en lugar de escribir datos escribes {} entonces se borraria absolutamente todo de datos.json y se escribiria solo {}
    #Lo dicho, esta funcion reemplaza todo lo que esta en el .json. Por eso basta con cargar todo el diccionario modificar lo que haya que modificar y sobreescribir el anterior.
    #Entiendo que para proyectos pequeños como este no hay mayores problemas, ya se solucionara este problema con las bases de datos de verdad I guess. 
    guardar_materia(datos)
    guardar_sesion(sesiones)

    return sesiones,round(duracion,2),datos
#-----------------------------------------------------------------Funciones usadas para ver el progreso------------------------------------------------------------------
