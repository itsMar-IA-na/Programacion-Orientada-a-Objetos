# Sistema Avanzado de Gestión de Inventario de Libros

## Descripción
Este proyecto implementa un **sistema de gestión de inventarios** para una tienda de libros, utilizando Programación Orientada a Objetos (POO) en Python.  
El sistema permite manejar los productos de manera eficiente mediante colecciones y asegura persistencia de datos en archivos de texto.

## Objetivos
- Aplicar los conceptos de POO para estructurar el programa.
- Utilizar colecciones de Python (listas y diccionarios) para organizar los libros.
- Implementar la lectura y escritura en archivos para almacenamiento persistente.
- Desarrollar un menú interactivo en consola que facilite el uso del sistema.

## Requisitos Implementados
- **Clase `Producto`**: atributos `ID`, `nombre`, `cantidad`, `precio`.
- **Clase `Inventario`**: utiliza listas para almacenar productos y permite:
  - Agregar nuevos libros.
  - Eliminar libros por ID.
  - Actualizar cantidad o precio.
  - Buscar libros por nombre.
  - Mostrar todos los libros.
- **Manejo de Archivos**: guarda y carga automáticamente el inventario desde `inventario.txt`.
- **Menú Interactivo**: facilita la interacción del usuario con el sistema.

## Archivos del Proyecto
- `producto.py`: define la clase `Producto`.
- `inventario.py`: contiene la clase `Inventario` y las operaciones sobre los libros.
- `menu.py`: menú interactivo para el usuario.
- `inventario.txt`: archivo de persistencia con datos de ejemplo.
- `README.md`: documentación del proyecto.

## Ejemplo de Uso
```bash
===== Sistema de Inventario de Libros =====
1. Agregar libro
2. Eliminar libro
3. Actualizar libro
4. Buscar libro por nombre
5. Mostrar inventario completo
6. Salir
Seleccione una opción:
