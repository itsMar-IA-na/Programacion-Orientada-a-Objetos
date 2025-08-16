# Proyecto: Sistema de Inventario de Libros (Semana 9)

## Descripción
Este proyecto implementa un sistema básico de **gestión de inventario** en Python, utilizando los principios de **Programación Orientada a Objetos (POO)**.  
El sistema está orientado a la administración de **libros en una tienda o biblioteca**, permitiendo controlar su registro, búsqueda y actualización.

Está dividido en tres archivos principales:  
- `producto.py`: Contiene la clase `Producto`, que en este caso representa a un libro.  
- `inventario.py`: Contiene la clase `Inventario`, encargada de gestionar la colección de libros.  
- `main.py`: Contiene el menú principal para interactuar con el sistema mediante consola.  

---

## Funcionalidades
1. **Agregar libro**: Registra un nuevo libro con ID, título, cantidad y precio.  
2. **Eliminar libro**: Permite borrar un libro del inventario mediante su ID.  
3. **Actualizar libro**: Permite modificar la cantidad y/o precio de un libro.  
4. **Buscar libro por título**: Encuentra libros que coincidan parcial o totalmente con el nombre ingresado.  
5. **Mostrar inventario**: Lista todos los libros registrados en el inventario.  
6. **Salir**: Finaliza el programa.  

---

## Ejemplo de ejecución en consola

```text
===== Sistema de Inventario de Libros (Semana 9) =====
1. Agregar libro
2. Eliminar libro
3. Actualizar libro
4. Buscar libro por título
5. Mostrar inventario completo
6. Salir
Seleccione una opción: 1

Ingrese el ID del libro: 301
Ingrese el título: Cien años de soledad
Ingrese la cantidad: 10
Ingrese el precio: 15.50

Libro 'Cien años de soledad' agregado correctamente.

===== Sistema de Inventario de Libros (Semana 9) =====
1. Agregar libro
2. Eliminar libro
3. Actualizar libro
4. Buscar libro por título
5. Mostrar inventario completo
6. Salir
Seleccione una opción: 5

Inventario actual:
ID: 301 | Título: Cien años de soledad | Cantidad: 10 | Precio: $15.50
