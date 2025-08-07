import tkinter as tk
import json
from tkinter import messagebox
import program_logic as pl
from tkinter import ttk

materias_global = pl.cargar_materias() #Esta funcion ya se encarga de manejar los errores como que no exista datos.Json o si esta vacio. Por ultimo nos carga los datos dentro.
sesiones_global = pl.cargar_sesiones()
frame_actual    = None
tarjetas_materias = {} #Para asociar cada tarjeta con su nombre y poder eliminarlas si el usuario lo desea.
tarjetas_sesion   = {} #Para asociar cada tarjeta con su nombre y poder eliminarlas si el usuario lo desea.

def actualizar_mensaje_vacio_materia():
    global mensaje_vacio_materias
    if not materias_global:
        if not mensaje_vacio_materias.winfo_exists():
            mensaje_vacio_materias = tk.Label(materias_frame, text="No tienes ninguna materia creada", font=("Helvetica", 12), fg="gray")
            mensaje_vacio_materias.place(relx=0.5, rely=0.5, anchor="center")
        else:
            mensaje_vacio_materias.place(relx=0.5, rely=0.5, anchor="center") #Esto se ejecuta si el objeto ya existe.
            #Si el objeto existe y no se esta mostrando en pantalla pues lo muestra, good.
            #Si el objeto existe y se está mostrando en pantalla no se genera un duplicado, simplemente se reemplaza el anterior place con este que como es el mismo pues no pasa nada.
            #Esto lo queremos porque al momento abrir el programa nosotros creamos los mensajes independientemente se muestren o no en pantalla. Esto es asi porque si
            #solo los creamos cuando se vayan a mostrar y luego intentamos llamar a esta funcion de actualizar el mensaje puede intentar usar el .wingo_exists() sobre una variable que
            #no existe, en conclusion, nos da error. Por esto necesitamos crear estos objetos mensaje independientemente si los mostramos o no al abrir el programa y con el contenido
            #de este bloque else nos aseguramos de que se muestre en pantalla cuando debe.
    else:
        if mensaje_vacio_materias.winfo_exists():
            mensaje_vacio_materias.destroy()

def actualizar_mensaje_vacio_sesion():
    global mensaje_vacio_sesiones
    if not sesiones_global:
        if not mensaje_vacio_sesiones.winfo_exists():
            mensaje_vacio_sesiones = tk.Label(sesiones_frame, text="No hay ninguna sesión activa", font=("Helvetica", 12), fg="gray")
            mensaje_vacio_sesiones.place(relx=0.5, rely=0.5, anchor="center")
        else:
            mensaje_vacio_sesiones.place(relx=0.5, rely=0.5, anchor="center")
    else:
        if  mensaje_vacio_sesiones.winfo_exists():
            mensaje_vacio_sesiones.destroy()    

def scroll_con_limite(event):

    if frame_actual == "materias":
        canvas = canvas_materias
    elif frame_actual == "sesiones":
        canvas = canvas_sesiones
    else:
        return  # no hay canvas visible

    # Lógica de límite
    first, last = canvas.yview()
    if event.delta < 0 and last < 1.0:
        canvas.yview_scroll(1, "units")
    elif event.delta > 0 and first > 0.0:
        canvas.yview_scroll(-1, "units")
#--------------------------------------------------------------------------------------------------Materias_frame_funciones-----------------------------------------------------------------------
def popup_creacion_materia():
    popup = tk.Toplevel()
    popup.title("Crear nueva materia")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set() #Este metodo es para impedir la interaccion con cualquier otra ventana que no sea popup. Esto bloquea la interaccion con materia_frame y con eso evita
    #que se pueda darle infinitas veces al boton de crear y se puedan llamar infinitas veces esta funcion, con esto tambien se evita que pueda darle al boton de regresar y que cambie
    #de frame. Y eso es lo que queremos porque el usuario debe lidiar primero con el popup antes de seguir usando el programa. Ademas trae la atencion sobre el popup, eso significa
    #que si intentas sobreponer materias_frame sobre el popup no podras, prevalecera el popup y es el que se mantendra siempre sobre materias_frame. Tambien forma parte del comportamiento
    #Deseado
    tk.Label(popup, text="Nombre de la materia:").pack(pady=(10, 0))

    entry_nombre = tk.Entry(popup)
    entry_nombre.pack(pady=(0, 10), ipadx=30)
    entry_nombre.focus_set() #Esto trae el focus sobre el entry al momento de que se abra el popup, es util en UX(user experience) porque le facilitamos la experiencia al usuario con el programa

    # Entrada para el objetivo en horas
    tk.Label(popup, text="Objetivo (horas):").pack()
    entry_horas = tk.Entry(popup)
    entry_horas.pack(pady=(0, 10), ipadx=30)

    def cancelar():
        popup.destroy()

    def crear(event = None):
        nombre = entry_nombre.get().strip().lower()
        horas = entry_horas.get().strip()
        materias = pl.cargar_materias()

        if not nombre or not horas.isdigit():
            messagebox.showerror("Error", "Nombre vacío u horas no numéricas.")
            change_focus_set()
            return
        # Aquí iría tu lógica para guardar la materia usando tus funciones:
        elif nombre in materias:            
            messagebox.showerror("Error", "La materia ya existe.")
            change_focus_set()
        else:
            horas = int(horas)
            if horas > 787500:
                messagebox.showerror("¿wtf?", "Eso son más de 90 años, ponga una cantidad real")
                return 1
            elif horas == 0:
                messagebox.showerror("Error", "No puedes poner de objetivo cero horas.")
                return 1
            if len(nombre) > 39:
                messagebox.showerror("Error","Por favor introduce un nombre con menos de 39 caracteres")
                return 1
            datos = pl.new_topic(nombre,horas)
            crear_tarjeta_materia(nombre)
            messagebox.showinfo("Éxito", "La materia ha sido creada exitosamente.")
            popup.destroy()
            #Reemplazamos el diccionario que se cargo al inicio con el nuevo diccionario que contiene al anterior mas el dato agregado.
            #Esto es para que este sincronizado, pero no tiene que ver con mostrar la materia en la pantalla
            global materias_global
            materias_global = datos
            actualizar_mensaje_vacio_materia()

    def change_focus_set():
        entry_nombre.focus_set()
       
    # Botones
    boton_cancelar = tk.Button(popup, text="❌", fg="white", bg="red", command=cancelar, cursor='hand2')
    boton_cancelar.place(x=20, y=160, width=40, height=30)

    boton_crear = tk.Button(popup, text="✔️", fg="white", bg="green", command=crear, cursor='hand2')
    boton_crear.place(x=240, y=160, width=40, height=30)

    #Events:
        #Cambiar entre entries usando las flechas del teclado:
    entry_nombre.bind('<Down>',lambda event: entry_horas.focus_set())
    entry_horas.bind('<Up>',lambda event: entry_nombre.focus_set())
        #Llamar a crear cuando el usuario presione enter:
    popup.bind('<Return>', crear)

def popup_materia(materia: str):
    global materias_global
    tiempo_acumulado = materias_global[materia]["tiempo_acumulado"]
    objetivo_horas = materias_global[materia]["objetivo_horas"]
    sesiones = materias_global[materia]["sesiones"]
    popup = tk.Toplevel()
    popup.title(f"{materia}")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set()
    button = tk.Button(popup,text="Eliminar materia", fg="white", bg="red", cursor='hand2', borderwidth=0)
    button.bind("<Button-1>", lambda event: popup_eliminar_materia(materia, popup))
    button.place(relx = 1.0, x=-102, y=10, anchor="nw")
    tk.Label(popup, text="Tiempo total:", font=('Helvetica',15)).pack(pady=(35, 0))
    tk.Label(popup, text=f"({tiempo_acumulado:.2f} / {objetivo_horas}) - horas", font=('Helvetica',10)).pack(pady=(5, 0))
    percentage_of_accomplishment = (tiempo_acumulado * 100) / (objetivo_horas)
    tk.Label(popup, text=f"{percentage_of_accomplishment:.2f} %").pack()
    tk.Label(popup, text="Última sesión:", font=('Helvetica',15)).pack(pady=(10, 0))
    if not sesiones:
        tk.Label(popup, text=f"Aún no tienes ninguna sesión registrada para {materia}", font=('Helvetica',8)).pack(pady=(10, 0))
    else:
        date_datetimeFormat = sesiones[-1]["fin"]
        date = date_datetimeFormat.split("T")[0]
        hour = date_datetimeFormat.split("T")[1][:5]
        tk.Label(popup, text=f"{date} - {hour} horas", font=('Helvetica',10)).pack(pady=(0, 0))

def popup_eliminar_materia(materia: str, popup_anterior: tk):
    popup = tk.Toplevel()
    popup.title(f"{materia}")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set()

    def cancelar():
        popup.destroy()
        popup_anterior.grab_set()
    def eliminar():
        global materias_global
        global sesiones_global
        try: 
            tarjetas_sesion[materia]
        except KeyError:  
            materias = pl.eliminiar_materia(materia)
            materias_global = materias
            messagebox.showinfo("Éxito", "La materia ha sido eliminada exitosamente.")
            popup.destroy()
            popup_anterior.destroy()
            tarjetas_materias[materia].destroy()
            del tarjetas_materias[materia]
            actualizar_mensaje_vacio_materia()
        else:
            sesiones, duracion, datos = pl.terminar_sesion(materia) #Con "datos" no hacemos nada. Si se ejecuta este Else quier decir
            #que existe una sesion de la materia que se piensa eliminar. Por tanto no es necesario guardar los datos globales con la sesion que se acaba de terminar porque
            #se va a proceder a eliminar la materia. Y si se elimina la materia tambien se elimina, si se da el caso, la sesion que tenga activa 
            materias = pl.eliminiar_materia(materia)
            sesiones_global = sesiones
            materias_global = materias
            messagebox.showinfo("Éxito", f"La materia ha sido eliminada exitosamente.\nEsta materia tenía una sesión activa con {duracion} horas\nDicha sesión también ha sido eliminada.")
            popup.destroy()
            popup_anterior.destroy()
            tarjetas_materias[materia].destroy()
            tarjetas_sesion[materia].destroy()
            del tarjetas_materias[materia]
            del tarjetas_sesion[materia]    
            actualizar_mensaje_vacio_materia()
            actualizar_mensaje_vacio_sesion()

    tk.Label(popup, text=f"¿Estás seguro de que deseas eliminar \n --{materia}--?\n Si eliminas esta materia: \n no habrá forma de recuperarla \n ¿estás seguro?", font=("Helvetica", 10)).pack(pady=30)
    boton_cancelar = tk.Button(popup, text="❌", fg="white", bg="red", command=cancelar, cursor='hand2')
    boton_cancelar.place(x=20, y=160, width=40, height=30)

    boton_crear = tk.Button(popup, text="✔️", fg="white", bg="green", command=lambda: eliminar(),cursor='hand2')
    boton_crear.place(x=240, y=160, width=40, height=30)    



def crear_tarjeta_materia(materia: str):
    tarjeta_m = tk.Frame(contenedor_tarjetas_materias, bd=1, relief="solid", padx=10, pady=5)
    tarjeta_m.pack(pady=5, padx=5, anchor="center")
    tarjeta_m.bind("<Button-1>", lambda event:popup_materia(materia))
    
    tarjetas_materias[materia] = tarjeta_m
    
    nombre = tk.Label(tarjeta_m, text=materia, font=("Helvetica", 12))
    nombre.pack()
    nombre.bind("<Button-1>", lambda event:popup_materia(materia))

    return tarjeta_m
# Crear la ventana principal

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------Sesiones_frame_funciones-----------------------------------------------------------------------
def popup_sesion(materia: str):
    popup = tk.Toplevel()
    popup.title("R. histórico de sesiones")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set()
    button = tk.Button(popup,text="Terminar sesión", fg="white", bg="red", cursor='hand2')
    button.bind("<Button-1>", lambda event: eliminar_sesion(materia, popup))
    button.place(relx = 1.0, x=-102, y=10, anchor="nw")
    sesiones_dictionary = materias_global[materia]["sesiones"]
    if len(sesiones_dictionary) == 0:
        tk.Label(popup, text="Cuando termines esta sesión activa la verás aquí\nEn el registro histórico de sesiones").place(relx=0.5, rely=0.5 ,anchor="center")
    else:
        for i, sesion in enumerate(sesiones_dictionary[::-1], start=1):
            if i >= 3:
                break
            tk.Label(popup, text=f"Sesión: {i}",font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))

            # Parsear y formatear las fechas
            inicio = sesion["inicio"].split("T")
            fin = sesion["fin"].split("T")

            inicio_fecha = inicio[0]
            inicio_hora = inicio[1][:5]  # solo hh:mm

            fin_fecha = fin[0]
            fin_hora = fin[1][:5]

            # Mostrar inicio
            tk.Label(popup, text=f"Inicio: {inicio_fecha}  /  {inicio_hora}", font=("Helvetica", 9)).pack(anchor="w", padx=20)
            # Mostrar fin
            tk.Label(popup, text=f"Fin:    {fin_fecha}  /  {fin_hora}", font=("Helvetica", 9)).pack(anchor="w", padx=20)

def popup_creacion_sesion(e =  None):
    popup = tk.Toplevel()
    popup.title("Crear nueva sesion")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set()
    tk.Label(popup, text="Seleccione la materia\n de la que quiere iniciar una sesion de estudio:").pack(pady=(10, 0))
    lista_materias = [a for a in materias_global]
    combo = ttk.Combobox(popup, values=lista_materias,state="readonly")
    combo.set("Selecciona una materia")
    combo.pack(pady=10)

    boton_cancelar = tk.Button(popup, text="❌", fg="white", bg="red", command=popup.destroy, cursor='hand2')
    boton_cancelar.place(x=20, y=160, width=40, height=30)

    boton_crear = tk.Button(popup, text="✔️", fg="white", bg="green", command=lambda: empezar_sesion(combo, popup), cursor='hand2')
    boton_crear.place(x=240, y=160, width=40, height=30)

def empezar_sesion(combo: ttk, popup):
    materia_seleccionada = combo.get()
    sesion = pl.iniciar_sesion(materia_seleccionada)
    if sesion != 1:
        messagebox.showinfo("Éxito", f"Se ha empeza una sesion de estudio para \n {materia_seleccionada}")
        global sesiones_global
        sesiones_global = sesion
        crear_tarjeta_sesion(materia_seleccionada)
        actualizar_mensaje_vacio_sesion()
        popup.destroy()
    else:
        messagebox.showerror("Error", "Esta materia ya tiene una sesion activa")

def crear_tarjeta_sesion(materia: str):
    tarjeta_s = tk.Frame(contenedor_tarjetas_sesiones, bd=1, relief="solid", padx=10, pady=5)
    tarjeta_s.pack(pady=5, padx=5, anchor="center")
    tarjeta_s.bind("<Button-1>", lambda event:popup_sesion(materia))
    
    tarjetas_sesion[materia] = tarjeta_s
    
    nombre = tk.Label(tarjeta_s, text=materia, font=("Helvetica", 12))
    nombre.pack()
    nombre.bind("<Button-1>", lambda event:popup_sesion(materia))

    return tarjeta_s

def eliminar_sesion(materia: str, popup_anterior: tk):
    sesiones,duracion,datos = pl.terminar_sesion(materia)
    global sesiones_global
    sesiones_global = sesiones
    global materias_global
    materias_global = datos
    messagebox.showinfo("Éxito", f"Has terminado la sesion de\n{materia}. Has acumulado {duracion} horas")
    popup_anterior.destroy()
    tarjetas_sesion[materia].destroy()
    del tarjetas_sesion[materia]
    actualizar_mensaje_vacio_sesion()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------Root----------------------------------------------------------------------------

root = tk.Tk()
try:
    icono = tk.PhotoImage(file="icon/icon.png")
    root.iconphoto(True,icono)
except Exception:
    pass
root.title("TopicManager")
screen_width = root.winfo_screenwidth()
screen_heigh = root.winfo_screenheight()
x_position = round(screen_width / 2 - 400 / 2)
y_position = round(screen_heigh / 2 - 300 / 2) - 70
root.geometry(f"400x300+{x_position}+{y_position}")  # tamaño de la ventana 
root.resizable(False, False) #Básicamente que no se pueda cambiar la resolución ni en altura ni en anchura
# Función para mostrar un frame y ocultar los demás

root.bind_all("<MouseWheel>", scroll_con_limite)

def mostrar_frame(frame: tk):
    global frame_actual
    frame.tkraise()
    if frame == materias_frame:
        frame_actual = "materias"
    elif frame == sesiones_frame:
        frame_actual = "sesiones"
    elif frame == inicio_frame:
        frame_actual = "inicio"    

# Crear los frames que serán nuestras pantallas
inicio_frame = tk.Frame(root)
materias_frame = tk.Frame(root)
sesiones_frame = tk.Frame(root)

canvas_materias = tk.Canvas(materias_frame)
canvas_materias.pack(side="left",fill="both", expand=True)

canvas_sesiones = tk.Canvas(sesiones_frame)
canvas_sesiones.pack(side="left",fill="both", expand=True)


contenedor_tarjetas_materias = tk.Frame(canvas_materias)
canvas_materias.create_window((0,0), window=contenedor_tarjetas_materias, anchor="nw", width=400) # Estamos diciendo que coloque sobre el lienzo el widget contenedor_tarjetas_materias en la posicion absoluta:(123,30)

contenedor_tarjetas_sesiones = tk.Frame(canvas_sesiones)
canvas_sesiones.create_window((123,0), window=contenedor_tarjetas_sesiones, anchor="nw", width=400)

for frame in (inicio_frame, materias_frame, sesiones_frame):    #Los frames son un tipo especial de widget, y como todo widget, su creación necesita de mayores especificaciones
    #En específico, el cómo y el dónde se colocará en pantalla, en términos prácticos se trata de usar uno de los 3 métodos geométricos integrados en tkinter y de no usarlos
    #Tkinter no sabe cómo ni dónde poner los widgets creados en la pantalla, así que simplemente no los mostrará. Aquí le estamos diciendo que los 3 frames los muestre como .place
    #que básicamente es que no se reescale, esto nos sirve porque prohibimos el cambio de dimensiones en anchura y altura antes por lo que no hay escenario por el que deba reescalarse.
    frame.place(relwidth=1, relheight=1)

# Contenido del frame de inicio
tk.Label(inicio_frame, text="Bienvenido al registro de estudio", font=("Helvetica", 14)).pack(pady=30)

tk.Button(inicio_frame, text="Materias", width=20, cursor='hand2', relief='groove', command=lambda: mostrar_frame(materias_frame)).pack(pady=10)
tk.Button(inicio_frame, text="Sesiones activas", width=20, cursor='hand2', relief='groove',command=lambda: mostrar_frame(sesiones_frame)).pack(pady=10)
#---------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------Materias frame------------------------------------------------------------------
mensaje_vacio_materias = tk.Label(materias_frame, text="No tienes ninguna materia creada", font=("Helvetica", 12), fg="gray",)
# Mensaje central (cuando no hay materias)
if not materias_global: #Esto ocurre si solo tenemos {}. Seria type None si no tuviera ni {}, pero eso es imposible. Llamando a pl.cargar_materias() ya nos encargamos de que sea imposible
    #Ser None y que con ello podamos leer los datos con json.load() adecuadamente. 
    mensaje_vacio_materias.place(relx=0.5, rely=0.5, anchor="center")
else:
    for materia in materias_global:
        crear_tarjeta_materia(materia)

# Botón atrás (esquina superior izquierda)
boton_atras_materias_frame = tk.Button(materias_frame, text="←", font=("Helvetica", 12), cursor='hand2', relief='groove', command=lambda: mostrar_frame(inicio_frame))
boton_atras_materias_frame.place(relx = 0,x=10, y=10, anchor='nw') #Siempre que se use una posicion relativa. Es relativa con respecto a que? Ese que es el anchor.
#nw es north west, ne: noth east. s: south... Y asi, Primero decimos 

# Botón crear (esquina superior derecha)
boton_crear_materias_frame = tk.Button(materias_frame, text="+", font=("Helvetica", 14), cursor='hand2', relief='groove', command=lambda: popup_creacion_materia())
boton_crear_materias_frame.place(relx = 1.0, x=-22, y=10, anchor="ne")

#Scrollbar:
scrollbar = tk.Scrollbar(materias_frame, orient="vertical", command=canvas_materias.yview)
scrollbar.pack(side="right", fill="y")
canvas_materias.config(yscrollcommand=scrollbar.set)
canvas_materias.bind("<Configure>", lambda event: canvas_materias.configure(scrollregion=canvas_materias.bbox("all")))
contenedor_tarjetas_materias.bind("<Configure>", lambda e: canvas_materias.configure(scrollregion=canvas_materias.bbox("all")))

#-------------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------Sesiones frame-------------------------------------------------------------------
mensaje_vacio_sesiones = tk.Label(sesiones_frame, text="No hay ninguna sesión activa", font=("Helvetica", 12), fg="gray")
if not sesiones_global: #Esto ocurre si solo tenemos {}. Seria type None si no tuviera ni {}, pero eso es imposible. Llamando a pl.cargar_sesiones() ya nos encargamos de que sea imposible
    #Ser None y que con ello podamos leer los datos con json.load() adecuadamente. 
    mensaje_vacio_sesiones.place(relx=0.5, rely=0.5, anchor="center")
else:
    for sesion in sesiones_global:
        crear_tarjeta_sesion(sesion)

boton_atras_sesiones_frame = tk.Button(sesiones_frame, text="←", font=("Helvetica", 12), cursor='hand2', relief='groove', command=lambda: mostrar_frame(inicio_frame))
boton_atras_sesiones_frame.place(relx = 0,x=10, y=10, anchor='nw')

boton_crear_sesiones_frame = tk.Button(sesiones_frame, text="+", font=("Helvetica", 14), cursor='hand2', relief='groove', command=lambda: popup_creacion_sesion())
boton_crear_sesiones_frame.place(relx = 1.0, x=-22, y=10, anchor="ne")
#Scrollbar:
scrollbar = tk.Scrollbar(sesiones_frame, orient="vertical", command=canvas_sesiones.yview)
scrollbar.pack(side="right", fill="y")
canvas_sesiones.config(yscrollcommand=scrollbar.set)
canvas_sesiones.bind("<Configure>", lambda event: canvas_sesiones.configure(scrollregion=canvas_sesiones.bbox("all")))
contenedor_tarjetas_sesiones.bind("<Configure>", lambda e: canvas_sesiones.configure(scrollregion=canvas_sesiones.bbox("all")))
#-----------------------------------------------------------------------------------------------------------------------------


# Mostrar frame de inicio al arrancar
mostrar_frame(inicio_frame)

root.mainloop()
