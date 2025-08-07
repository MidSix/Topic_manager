# TopicManager (Working Title)

## 🇬🇧 ---English----

This is a personal project that I found really useful and exciting to develop.

I got inspired by the way **Steam** tracks how many hours you've spent playing a game. For those who don't know, Steam is a massive gaming platform for PC users that logs every session of a game and shows you the total playtime.

At least for me, it's quite addictive to see how those hours go up. It's a visible way to measure the **effort you've invested**, even if results aren't showing up yet. I think that's gold — because many people give up before they realize how much work they've already done, and that can be truly sad.

This small tool tries to bring that same idea to study and personal projects: to track how much time you've dedicated to a specific subject or task, session by session.

Whether you're a student, a developer, or just someone working towards a long-term goal, **seeing the hours add up** can help you stay motivated and remind you that every small session counts.

## Features (Completed)

- Track time spent on study sessions per subject
- Add and manage different topics
- Store session logs with start/end time
- View total time accumulated
- Built using pure Python and JSON for simplicity, at least for now.

## Guide – How to Use TopicManager

1. **Run the program**  
   Just double-click `TopicManager.exe`. No installation is required — it works as a portable app.

2. **Add a new subject**  
   Go to the "Subjects" section and click the + button. You must assign a name and set an **hour-based goal**.

3. **Start a study session**  
   Switch to the "Active sessions" section. Click the + button to start a session. A dropdown list will appear where you must select one of your existing subjects. Once selected, press the green button to begin tracking time.

4. **Stop a session**  
   In the "Active essions" section, click the subject you want to stop and press the "End session" button.

5. **Delete a subject**  
   From the "Subjects" section, click the desired subject and then press his red button to delete it. If it has an active session, that session will be stopped and removed as well.

6. **See your progress**  
   - In the "Subjects" section, click on any subject to view the **total hours studied** and the **Last registered session** (A session is registered once it's finished).  
   - In the "Active sessions" section, click on a subject to see the **history of the last two sessions**.

7. **Where your data is saved**  
   Session and subject data is stored locally in JSON format. No data is sent to the cloud.

## Disclaimer

This is an MVP and a learning project. I'm building it as I go to improve my skills and explore ideas. Contributions and suggestions are welcome.

## 🇪🇸 ---Español---

Este es un proyecto personal que me pareció útil y emocionante de desarrollar.

Me inspiré en la forma en que **Steam** registra cuántas horas has jugado a un videojuego. Para quienes no lo conozcan, Steam es una plataforma enorme de videojuegos para usuarios de PC que guarda un registro de cada sesión y te muestra el tiempo total jugado.

Al menos para mí, es bastante adictivo ver cómo esas horas aumentan. Es una forma visual de medir el **esfuerzo que has invertido**, incluso cuando los resultados aún no se ven. Y eso me parece oro — porque mucha gente se rinde sin tener una medida de cuánto tiempo han invertido ya, y eso es ser muy triste.

Esta pequeña herramienta busca llevar esa misma idea al estudio o a proyectos personales: registrar cuánto tiempo has dedicado a una materia o tarea concreta, sesión por sesión.

Tanto si eres estudiante, desarrollador o alguien que trabaja en un objetivo a largo plazo, **ver cómo se acumulan las horas** puede ayudarte a mantenerte motivado y recordarte que cada sesión cuenta.

### Funcionalidades (Completadas)

- Registrar el tiempo dedicado por materia
- Añadir y gestionar materias
- Guardar sesiones con hora de inicio y fin
- Consultar el tiempo total acumulado
- Hecho con Python puro y JSON por simplicidad

## Guía de uso – Cómo usar TopicManager

1. **Ejecutar el programa**  
   Haz doble clic en `TopicManager.exe`. No requiere instalación: es una aplicación portable.

2. **Añadir una materia**  
   Ve a la sección "Materias" y pulsa el botón +. Debes asignar un nombre y establecer un **objetivo de horas**.

3. **Iniciar una sesión de estudio**  
   Cambia a la sección "Sesiones activas". Pulsa el botón + para iniciar una nueva sesión. Aparecerá un menú desplegable donde debes seleccionar una de las materias existentes. Una vez seleccionada, pulsa el botón verde para comenzar a registrar el tiempo.

4. **Detener una sesión**  
   En la sección "Sesiones activas", haz clic sobre la materia que deseas detener y pulsa el botón "Terminar sesión".

5. **Eliminar una materia**  
   Desde la sección "Materias", haz clic en la materia deseada y luego pulsa su botón rojo para eliminarla. Si tiene una sesión activa, esta también se detendrá y eliminará.

6. **Ver tu progreso**  
   - En la sección "Materias", haz clic en cualquier materia para ver el **total de horas estudiadas** y la **última sesión registrada** (una sesión se registra cuando finaliza).  
   - En la sección "Sesiones activas", haz clic en una materia para ver el **historial de las dos últimas sesiones**.

7. **Dónde se guarda tu información**  
   Los datos de materias y sesiones se guardan localmente en formato JSON. No se envía nada a la nube.
"""

## Disclaimer

Este es un producto mínimo viable, algo extramadamente sencillo que cumple con las funcionalidades mínimas necesarias. Además es un proyecto que estoy usando para aprender, lo
estoy haciendo mientras mis habilidades van mejorando y mientras aprendo cosas nuevas por lo que la implementación de varias funcionalidades puede y seguramente cambie. Todas
Las contribuciones y sugerencias son bienvenidas.
