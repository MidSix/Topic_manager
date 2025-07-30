import json
import os
from datetime import datetime
#-----------------------------------------------------------Funciones usadas para opcion 1---------------------------------------------------------------------------------
ARCHIVO_DATOS = "datos.json"
TEMP = "temp.json" #En temp.json están las materias que tienen sesiones abiertas.
def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS) or os.path.getsize(ARCHIVO_DATOS) == 0:    #Manejo de errores:
        #Si el archivo no existe en el cwd(current work directory) entrará en el condicional, si existe pero está vacío completamente también entrará en el condicional
        #tras entrar creará ARCHIVO_DATOS, para el caso por default: datos.json con y le escribirá un diccionario vacío porque si se intenta cargar con load 
        #un .json vacío sin siquiera un {} dará error porque el método espera que al menos tenga un diccionario vacío para cargar datos. Si existe pero está vacío
        #entonces lógicamente no creará el archivo sino que solo entrará en él y escribirá un {} para que funcione load después.
        with open(ARCHIVO_DATOS, "w") as file:
            json.dump({}, file)

    with open(ARCHIVO_DATOS, "r") as archivo:
        return json.load(archivo)

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def new_topic():
    nombre = input(" Nombre de la materia: ").lower()
    datos = cargar_datos()
    
    if nombre in datos: #Aquí recorremos las claves del diccionario datos, cada clave es una materia, si nombre es clave quiere decir que esa materia ya ha sido añadida
        #Simplemente hay que recordar que al recorrer diccionarios iteramos sobre las claves por defecto.
        print("Esa materia ya existe.")
        return 1
    
    objetivo = float(input("¿Cuántas horas quieres dedicarle? "))

    nueva_materia = {
        "objetivo_horas": objetivo,
        "tiempo_acumulado": 0.0,
        "sesiones": []
    }

    datos[nombre] = nueva_materia   #Estamos añadiendo un par clave-valor al diccionario.
    guardar_datos(datos)    #Guardamos en el Json el diccionario con el nuevo par clave-valor que acabamos de crear.

    print(f"Materia '{nombre}' añadida correctamente.")
    return 0
#--------------------------------------------------------Funciones usadas para opcion 2-----------------------------------------------------------------------------------------------------------------

def iniciar_sesion():
    materia = input(" ¿Cuál materia quieres empezar a hacer? ").lower()

    if not os.path.exists(TEMP) or os.path.getsize(TEMP) == 0:
        with open(TEMP, "w") as temp:
            json.dump({}, temp)

    with open(TEMP, "r") as tmp:
        temp = json.load(tmp)

    if not materia in temp:
        datos = cargar_datos()
        if materia in datos:
            temp[materia] = datetime.now().isoformat()    #Con esto añadimos el par clave valor con la materia como clave y la fecha de inicio como valor.
            #Sin .isoformat devuelve un objeto tipo datetime pero para guardarlo en nuestro .json necesitamos que sea un string. Isoformat se encarga de pasar el objeto datetime
            #Y pasarlo a string. 
            with open(TEMP, "w") as tmp:
                json.dump(temp, tmp)

            momento = datetime.fromisoformat(temp[materia])    #Esto se hace para tener un objeto tipo datetime y con ello poder usar el metodo de abajo.
            #Partimos del isoformat que es el string y lo pasamos de nuevo como objeto tipo datetime.
            print(f" Sesión iniciada para '{materia}' a las {momento.strftime('%H:%M:%S')}")

        else:
            print("materia no encontrada")
    else:
        print("Esta materia ya tiene una sesión abierta")
#-----------------------------------------------------------------Funciones usadas para opcion 3------------------------------------------------------------------
def terminar_sesion():
    if os.path.getsize(TEMP) == 0:
        print("No hay ninguna sesión activa")
        return 1
    materia = input("¿Cuál sesión quieres terminar? ").lower()

    with open(TEMP, "r") as temp:
        sesiones = json.load(temp)

    with open(ARCHIVO_DATOS, "r") as datosfile:
        datos = json.load(datosfile)

    momento_final = datetime.now() #Aqui no usamos el isoformat method, entonces al objeto en memoria que apunta el identificador momento_final es tipo datetime y no string.
    #---Para hacer operaciones como restas, sumas y demas entre fechas tenemos que tener los dos objetos tipo datetime, porque esos objetos tendran ahi sus metodos para 
    #Manejar estas operaciones.
    if materia in sesiones:
        momento_inicial = sesiones[materia] #Lo carga desde el diccionario cargado a este modulo  de temp.Json, por lo tanto es de tipo string. Hemos de pasarlo a datetime.
    momento_inicial = datetime.fromisoformat(momento_inicial)
    duracion = (momento_final - momento_inicial).total_seconds() / 3600 # en horas.
    #Actualizacion del diccionario:
    datos[materia]["tiempo_acumulado"] += duracion
    datos[materia]["sesiones"].append({
        "inicio": momento_inicial.isoformat(),
        "fin"   : momento_final.isoformat()
    })
    #Con esto sobreescribimos datos. / si en lugar de escribir datos escribes {} entonces se borraria absolutamente todo de datos.json y se escribiria solo {}
    #Lo dicho, esta funcion reemplaza todo lo que esta en el .json. Por eso basta con cargar todo el diccionario modificar lo que haya que modificar y sobreescribir el anterior.
    #Entiendo que para proyectos pequeños como este no hay mayores problemas, ya se solucionara este problema con las bases de datos de verdad I guess. 
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(datos, f, indent=4)

    del(sesiones[materia])

    with open(TEMP, "w") as tmp:
        json.dump(sesiones, tmp)

    print(f" Sesión terminada. Has sumado {duracion:.2f} horas a '{materia}'")
#-----------------------------------------------------------------Funciones usadas para opcion 4------------------------------------------------------------------
def progreso():
    materia = input("¿De qué materia quieres saber sus horas acumuladas? ").lower()
    with open(ARCHIVO_DATOS, "r") as f:
        datos = json.load(f)
    if materia in datos:
        print(f"{datos[materia]["tiempo_acumulado"]:.1f} h acumuladas.")
        return 0
    else:
        print("La materia no existe")
        return 1
