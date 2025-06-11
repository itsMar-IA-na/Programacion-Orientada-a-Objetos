# Clase que representa un libro
class Libro:
    def __init__(self, codigo, titulo, autor):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.disponible = True  # Estado del libro

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def devolver(self):
        self.disponible = True

# Clase que representa un lector de la biblioteca
class Usuario:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula
        self.libros_prestados = []  # Lista de libros prestados

    def tomar_prestado(self, libro):
        if libro.prestar():
            self.libros_prestados.append(libro)
            print(f"{self.nombre} ha prestado el libro '{libro.titulo}'.")
        else:
            print(f"El libro '{libro.titulo}' no está disponible.")

    def devolver_libro(self, codigo_libro):
        for libro in self.libros_prestados:
            if libro.codigo == codigo_libro:
                libro.devolver()
                self.libros_prestados.remove(libro)
                print(f"{self.nombre} devolvió el libro '{libro.titulo}'.")
                return
        print(f"{self.nombre} no tiene ese libro prestado.")

# Clase que representa la biblioteca
class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []
        self.usuarios = []

    def agregar_libro(self, libro):
        self.catalogo.append(libro)

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def mostrar_disponibles(self):
        print(f"Libros disponibles en {self.nombre}:")
        for libro in self.catalogo:
            if libro.disponible:
                print(f"{libro.codigo} - '{libro.titulo}' de {libro.autor}")

    def buscar_libro_por_codigo(self, codigo):
        for libro in self.catalogo:
            if libro.codigo == codigo:
                return libro
        return None

# Simulación del sistema
# Crear biblioteca
biblio = Biblioteca("Biblioteca Y Libreria Mariana")

# Agregar libros
biblio.agregar_libro(Libro("M301", "Cien años de soledad", "Gabriel García Márquez"))
biblio.agregar_libro(Libro("M432", "El misterio del Colegio Embrujado", "Ulises Cabal"))
biblio.agregar_libro(Libro("M232", "Don Quijote", "Miguel de Cervantes"))
biblio.agregar_libro(Libro("M157", "El principito", "Antoine de Saint-Exupéry"))
biblio.agregar_libro(Libro("M843", "La culpa es de la vaca", "Jaime Lopera y Marta Bernal"))

# Registrar usuarios
u1 = Usuario("Mariana López", "0952602464")
u2 = Usuario("Teresa Andrade", "1744534565")
biblio.registrar_usuario(u1)
biblio.registrar_usuario(u2)

# Mostrar libros disponibles
biblio.mostrar_disponibles()

# u1 toma prestado un libro
libro_a_prestar = biblio.buscar_libro_por_codigo("M232")
if libro_a_prestar:
    u1.tomar_prestado(libro_a_prestar)

# u2 intenta tomar el mismo libro (debería fallar)
u2.tomar_prestado(libro_a_prestar)

# u1 devuelve el libro
u1.devolver_libro("M232")

# Ahora u2 intenta de nuevo
u2.tomar_prestado(libro_a_prestar)

# Mostrar libros disponibles al final
biblio.mostrar_disponibles()
