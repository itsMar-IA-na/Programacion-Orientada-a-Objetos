## Introducción
Este proyecto consiste en un **sistema de gestión de inventario de libros** desarrollado con el lenguaje **Python** y la librería **Tkinter** para la interfaz gráfica.  
El objetivo fue crear una herramienta visual y sencilla que permita **registrar, editar, eliminar y almacenar libros**, además de **importar y exportar** los datos en formato **CSV** para su respaldo o uso externo.  

El sistema fue pensado para simular un pequeño inventario de biblioteca o librería, donde se puedan manejar los libros disponibles, su información y el control de existencias de forma práctica.  

---

## Funcionamiento general (pestaña de ejecución)
Al ejecutar el programa (`python sistema_libros.py`), se abre una **ventana principal** titulada “Sistema de Gestión de Libros”.  
Desde esta interfaz se puede realizar todo el manejo del inventario.  
En la parte superior aparecen los **campos de registro**, luego los **botones de acción**, y finalmente la **tabla** que muestra todos los libros guardados.  

En la parte inferior hay una **barra de estado** que indica las acciones realizadas, por ejemplo:  
> Libro agregado correctamente  
> Último guardado: 14:35:22  
> Campos limpiados  

---

## Explicación de los botones y su utilidad

| **Botón** | **Función** |
|:-----------|:------------|
| **Agregar** | Permite añadir un nuevo libro al inventario. Se deben completar los campos de ID y título (mínimo). |
| **Editar** | Modifica los datos del libro seleccionado en la tabla. Solo se reflejarán los cambios al presionar “Guardar cambios”. |
| **Eliminar** | Quita el libro seleccionado de la tabla. La eliminación será definitiva una vez guardados los cambios. |
| **Guardar cambios** | Guarda todos los datos actuales de la tabla en el archivo CSV principal (`libros.csv`). También actualiza la hora del último guardado. |
| **Importar CSV** | Permite importar datos desde otro archivo CSV. Los libros nuevos se combinan con los ya existentes. |
| **Exportar CSV** | Crea un nuevo archivo CSV con la información actual de la tabla, útil como copia de respaldo. |
| **Limpiar campos** | Borra todo el contenido de los cuadros de texto del formulario, ideal para registrar un nuevo libro desde cero. |

---

## Estructura del archivo principal
El código está organizado en tres clases principales:

### 1. Clase `Libro`
Define la estructura de un libro (**ID**, **título**, **autor**, **editorial**, **cantidad**, **precio**, etc.).  
Sirve como modelo para representar cada registro del inventario.  

### 2. Clase `GestorLibros`
Se encarga de manejar el archivo CSV donde se almacenan los datos.  
Contiene funciones para guardar, cargar, importar y exportar la información.  

### 3. Clase `InterfazPrincipal`
Es la parte visual del programa. Aquí se definen los **botones**, la **tabla** y todos los **eventos** que responden a las acciones del usuario.  

Finalmente, al final del código se encuentra la sección:
```python
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazPrincipal(ventana)
    ventana.mainloop()
