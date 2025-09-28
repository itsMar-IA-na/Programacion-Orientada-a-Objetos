# Lista de Tareas en Tkinter

Aplicación de escritorio hecha con **Python y Tkinter** para gestionar tus tareas.

## Características
- Añadir nuevas tareas con prioridad y fecha de vencimiento
- Marcar tareas como completadas o pendientes (doble clic o botón)
- Eliminar tareas seleccionadas
- Filtrar por estado (todas, activas, completadas)
- Filtrar por prioridad (baja, normal, alta)
- Buscar tareas por texto o fecha
- Importar y exportar tareas en formato CSV
- Cargar ejemplos de tareas

## Cómo usar
1. Escribe una tarea en el campo de texto.
2. Selecciona la prioridad (Baja, Normal o Alta).
3. (Opcional) Define la fecha de vencimiento.
4. Haz clic en **Añadir** para guardarla.

### Acciones rápidas
- Doble clic en una tarea → marcar como completada o pendiente
- Tecla **Delete** → elimina las tareas seleccionadas
- Ctrl+N → enfoca el cuadro de texto para añadir nueva tarea

## Requisitos
- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones)
- Opcional: tkcalendar (`pip install tkcalendar`) para seleccionar fechas con calendario

## Notas
- Las tareas se guardan automáticamente en `tasks_data.json`.
- El README se genera automáticamente cada vez que se ejecuta el programa.
