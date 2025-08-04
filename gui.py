import tkinter as tk
import json
from tkinter import messagebox
import program_logic as pl
DATOS = "datos.json"

materias_global = pl.cargar_datos() #Esta funcion ya se encarga de manejar los errores como que no exista datos.Json o si esta vacio. Por ultimo nos carga los datos dentro.
tarjetas_materias = {} #Para asociar cada tarjeta con su nombre y poder eliminarlas si el usuario lo desea.

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
        with open(DATOS, 'r') as f:
            materias = json.load(f)

        if len(nombre) == 0 or not horas.isdigit():
            messagebox.showerror("Error", "Nombre vacío u horas no numéricas.")
            change_focus_set()
            return
        # Aquí iría tu lógica para guardar la materia usando tus funciones:
        elif nombre in materias:            
            messagebox.showerror("Error", "La materia ya existe.")
            change_focus_set()
        else:
            datos = pl.new_topic(nombre,horas)
            crear_tarjeta_materia(nombre)
            messagebox.showinfo("Éxito", "La materia ha sido creada exitosamente.")
            change_focus_set()
            #Reemplazamos el diccionario que se cargo al inicio con el nuevo diccionario que contiene al anterior mas el dato agregado.
            #Esto es para que este sincronizado, pero no tiene que ver con mostrar la materia en la pantalla
            global materias_global
            materias_global = datos
            entry_nombre.delete(0, tk.END)
            entry_horas.delete(0, tk.END)

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
    popup = tk.Toplevel()
    popup.title(f"{materia}")
    popup.geometry(f"300x200+{x_position}+{y_position}")
    popup.resizable(False, False)
    popup.grab_set()
    button = tk.Button(popup,text="❌", fg="white", bg="red", cursor='hand2')
    button.bind("<Button-1>", lambda event: popup_eliminar_materia(materia, popup))
    button.place(relx = 1.0, x=-22, y=10, anchor="ne")
    tk.Label(popup, text="Tiempo total:", font=('Helvetica',15)).pack(pady=(35, 0))
    tk.Label(popup, text=f"{materias_global[materia]["tiempo_acumulado"]:.2f} horas", font=('Helvetica',10)).pack(pady=(5, 0))
    tk.Label(popup, text="Última sesión:", font=('Helvetica',15)).pack(pady=(10, 0))
    if len(materias_global[materia]["sesiones"]) == 0:
        tk.Label(popup, text=f"Aún no tienes ninguna sesión registrada para {materia}", font=('Helvetica',8)).pack(pady=(10, 0))
    else:
        date_datetimeFormat = materias_global[materia]["sesiones"][-1]["fin"]
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
        materias = pl.eliminiar_materia(materia)
        global materias_global
        materias_global = materias
        messagebox.showinfo("Éxito", "La materia ha sido eliminada exitosamente.")
        popup.destroy()
        popup_anterior.destroy()
        tarjetas_materias[materia].destroy()
        del tarjetas_materias[materia]



    tk.Label(popup, text=f"¿Estás seguro de que deseas eliminar \n --{materia}--?\n Si eliminas esta materia: \n no habrá forma de recuperarla \n ¿estás seguro?", font=("Helvetica", 10)).pack(pady=30)
    boton_cancelar = tk.Button(popup, text="❌", fg="white", bg="red", command=cancelar, cursor='hand2')
    boton_cancelar.place(x=20, y=160, width=40, height=30)

    boton_crear = tk.Button(popup, text="✔️", fg="white", bg="green", command=eliminar,cursor='hand2')
    boton_crear.place(x=240, y=160, width=40, height=30)    



def crear_tarjeta_materia(materia: str):
    tarjeta = tk.Frame(contenedor_tarjetas, bd=1, relief="solid", padx=10, pady=5)
    tarjeta.pack(pady=5, padx=5)
    tarjeta.bind("<Button-1>", lambda event:popup_materia(materia))
    
    tarjetas_materias[materia] = tarjeta
    
    nombre = tk.Label(tarjeta, text=materia, font=("Helvetica", 12))
    nombre.pack()
    nombre.bind("<Button-1>", lambda event:popup_materia(materia))

    return tarjeta
# Crear la ventana principal
#------------------------------------------Root----------------------------------------------------------------------------

root = tk.Tk()
root.title("TopicManager")
screen_width = root.winfo_screenwidth()
screen_heigh = root.winfo_screenheight()
x_position = round(screen_width / 2 - 400 / 2)
y_position = round(screen_heigh / 2 - 300 / 2) - 70
root.geometry(f"400x300+{x_position}+{y_position}")  # tamaño de la ventana 
root.resizable(False, False) #Básicamente que no se pueda cambiar la resolución ni en altura ni en anchura
# Función para mostrar un frame y ocultar los demás
def mostrar_frame(frame):
    frame.tkraise()

# Crear los frames que serán nuestras pantallas
inicio_frame = tk.Frame(root)
materias_frame = tk.Frame(root)
sesiones_frame = tk.Frame(root)
canvas = tk.Canvas(materias_frame)
canvas.pack(side="left",fill="both", expand=True) 


contenedor_tarjetas = tk.Frame(canvas)
canvas.create_window((123,0), window=contenedor_tarjetas, anchor="nw") # Estamos diciendo que coloque sobre el lienzo el widget contenedor_tarjetas en la posicion absoluta:(123,30)


for frame in (inicio_frame, materias_frame, sesiones_frame):    #Los frames son un tipo especial de widget, y como todo widget, su creación necesita de mayores especificaciones
    #En específico, el cómo y el dónde se colocará en pantalla, en términos prácticos se trata de usar uno de los 3 métodos geométricos integrados en tkinter y de no usarlos
    #Tkinter no sabe cómo ni dónde poner los widgets creados en la pantalla, así que simplemente no los mostrará. Aquí le estamos diciendo que los 3 frames los muestre como .place
    #que básicamente es que no se reescale, esto nos sirve porque prohibimos el cambio de dimensiones en anchura y altura antes por lo que no hay escenario por el que deba reescalarse.
    frame.place(relwidth=1, relheight=1)

# Contenido del frame de inicio
tk.Label(inicio_frame, text="Bienvenido al registro de estudio", font=("Helvetica", 14)).pack(pady=30)

tk.Button(inicio_frame, text="Materias", width=20, cursor='hand2', relief='groove', command=lambda: mostrar_frame(materias_frame)).pack(pady=10)
tk.Button(inicio_frame, text="Sesiones", width=20, cursor='hand2', relief='groove',command=lambda: mostrar_frame(sesiones_frame)).pack(pady=10)
#------------------------------------------Root----------------------------------------------------------------------------

#------------------------------------------Materias frame------------------------------------------------------------------
# Mensaje central (cuando no hay materias)
if len(materias_global) == 0: #Esto ocurre si solo tenemos {}. Seria type None si no tuviera ni {}, pero eso es imposible. Llamando a pl.cargar_datos() ya nos encargamos de que sea imposible
    #Ser None y que con ello podamos leer los datos con json.load() adecuadamente. 
    mensaje_vacio = tk.Label(materias_frame, text="No tienes ninguna materia creada", font=("Helvetica", 12), fg="gray")
    mensaje_vacio.place(relx=0.5, rely=0.5, anchor="center")
else:
    for materia in materias_global:
        crear_tarjeta_materia(materia)

# Botón atrás (esquina superior izquierda)
boton_atras = tk.Button(materias_frame, text="←", font=("Helvetica", 12), cursor='hand2', relief='groove', command=lambda: mostrar_frame(inicio_frame))
boton_atras.place(relx = 0,x=10, y=10, anchor='nw') #Siempre que se use una posicion relativa. Es relativa con respecto a que? Ese que es el anchor.
#nw es north west, ne: noth east. s: south... Y asi, Primero decimos 

# Botón crear (esquina superior derecha)
boton_crear = tk.Button(materias_frame, text="+", font=("Helvetica", 14), cursor='hand2', relief='groove', command=lambda: popup_creacion_materia())
boton_crear.place(relx = 1.0, x=-22, y=10, anchor="ne")

#Scrollbar:
scrollbar = tk.Scrollbar(materias_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
contenedor_tarjetas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#------------------------------------------Materias frame------------------------------------------------------------------


#-------------------------------------------Sesiones frame-------------------------------------------------------------------
# Contenido inicial de sesiones_frame (también lo completaremos luego)
tk.Label(sesiones_frame, text="Aquí irán tus sesiones").pack()
#-------------------------------------------Sesiones frame-------------------------------------------------------------------


# Mostrar frame de inicio al arrancar
mostrar_frame(inicio_frame)

root.mainloop()
