from program_logic import new_topic, iniciar_sesion, terminar_sesion, progreso
active_sesions = {}
while True:
    print("\n1. Crear materia\n2. Iniciar sesión\n3. Terminar sesión\n4. Ver progreso\n0. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        new_topic()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        terminar_sesion()
    elif opcion == "4":
        progreso()
    elif opcion == "0":
        break
    else:
        raise Exception("Opción no válida")
