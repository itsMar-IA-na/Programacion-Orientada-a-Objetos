# Sistema de Gestión de Biblioteca Digital  

## 1. Introducción  
El presente proyecto corresponde al desarrollo de un **Sistema de Gestión de Biblioteca Digital**, cuyo propósito es ofrecer una solución orientada a objetos para la administración de recursos bibliográficos, usuarios y préstamos en un entorno académico.  
El sistema simula las operaciones básicas de una biblioteca moderna, permitiendo registrar usuarios, añadir o eliminar libros, gestionar préstamos y devoluciones, así como realizar búsquedas eficientes en el catálogo digital.  

La propuesta se fundamenta en el uso de estructuras de datos adecuadas (`listas`, `diccionarios`, `conjuntos` y `tuplas`) que optimizan la gestión de información y aseguran la integridad de los datos.  

---

## 2. Objetivo General  
Desarrollar un sistema modular en Python que gestione de manera eficiente los recursos de una biblioteca digital, integrando mecanismos de registro, control de préstamos y búsquedas en el catálogo.  

### Objetivos Específicos  
- Modelar los libros, usuarios y la biblioteca a través de **clases bien estructuradas**.  
- Implementar **operaciones CRUD** (crear, leer, actualizar, eliminar) para usuarios y libros.  
- Garantizar la **unicidad de los identificadores de usuarios** mediante el uso de conjuntos.  
- Permitir el control de préstamos y devoluciones a través de listas dinámicas.  
- Implementar un **módulo de búsqueda flexible** que soporte consultas por título, autor y categoría.  
- Probar el sistema con ejemplos prácticos de uso.  

---

## 3. Requisitos del Sistema  
- **Lenguaje de programación**: Python 3.8 o superior.  
- **Paradigma**: Programación Orientada a Objetos (POO).  
- **Estructuras de datos empleadas**:  
  - `Tuplas`: almacenamiento inmutable de título y autor en la clase `Libro`.  
  - `Listas`: gestión de libros prestados a cada usuario.  
  - `Diccionarios`: acceso eficiente a los libros por ISBN y usuarios por ID.  
  - `Conjuntos`: verificación de unicidad en los IDs de usuarios.  

---

## 4. Diseño del Sistema  

### 4.1. Clases Principales  

- **Clase `Libro`**  
  Representa un recurso bibliográfico. Contiene los atributos: título, autor, categoría e ISBN. El título y el autor se almacenan en una tupla, garantizando su inmutabilidad.  

- **Clase `Usuario`**  
  Define a los miembros de la biblioteca. Cada usuario posee un nombre, un identificador único y una lista de libros actualmente prestados.  

- **Clase `Biblioteca`**  
  Constituye el núcleo del sistema. Administra colecciones de libros y usuarios, asegurando la integridad de los registros y gestionando los procesos de préstamo, devolución, registro y búsqueda.  

### 4.2. Principales Métodos Implementados  
- `añadir_libro()` / `quitar_libro()`: gestión del inventario.  
- `registrar_usuario()` / `dar_baja_usuario()`: gestión de usuarios.  
- `prestar_libro()` / `devolver_libro()`: control de préstamos.  
- `buscar_libros()`: búsqueda por título, autor o categoría.  
- `listar_libros_prestados()`: consulta del estado de préstamos por usuario.  

---

## 5. Ejemplo de Uso  

```python
# Crear biblioteca
biblio = Biblioteca()

# Registrar libros
biblio.añadir_libro(Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "111"))
biblio.añadir_libro(Libro("El Quijote", "Miguel de Cervantes", "Clásico", "222"))

# Registrar usuarios
usuario = Usuario("Ana", "U01")
biblio.registrar_usuario(usuario)

# Prestar y devolver libros
biblio.prestar_libro("U01", "111")
biblio.listar_libros_prestados("U01")
biblio.devolver_libro("U01", "111")

#fin