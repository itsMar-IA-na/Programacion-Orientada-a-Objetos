"""
Sistema de Gestión de Biblioteca Digital
Proyecto académico universitario - 2025
"""

import logging
from typing import Dict, List, Set

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


class UsuarioNoEncontrado(Exception): pass
class LibroNoDisponible(Exception): pass
class PrestamoInvalido(Exception): pass


class Libro:
    """Representa un libro de la biblioteca."""

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str) -> None:
        self.datos = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self) -> str:
        return f"{self.datos[0]} - {self.datos[1]} (Categoría: {self.categoria}, ISBN: {self.isbn})"


class Usuario:
    """Representa un usuario de la biblioteca."""

    def __init__(self, nombre: str, id_usuario: str) -> None:
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados: List[Libro] = []
        self.historial_prestamos: List[Libro] = []

    def __str__(self) -> str:
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


class Biblioteca:
    """Gestiona los recursos, usuarios y préstamos de la biblioteca."""

    def __init__(self) -> None:
        self.libros: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.ids_usuarios: Set[str] = set()

    def añadir_libro(self, libro: Libro) -> None:
        if libro.isbn in self.libros:
            logging.warning("El libro ya existe.")
        else:
            self.libros[libro.isbn] = libro
            logging.info(f"Libro añadido: {libro}")

    def quitar_libro(self, isbn: str) -> None:
        if isbn not in self.libros:
            raise LibroNoDisponible("No se encontró un libro con ese ISBN.")
        eliminado = self.libros.pop(isbn)
        logging.info(f"Libro eliminado: {eliminado}")

    def registrar_usuario(self, usuario: Usuario) -> None:
        if usuario.id_usuario in self.ids_usuarios:
            logging.warning("El ID de usuario ya está registrado.")
        else:
            self.usuarios[usuario.id_usuario] = usuario
            self.ids_usuarios.add(usuario.id_usuario)
            logging.info(f"Usuario registrado: {usuario}")

    def dar_baja_usuario(self, id_usuario: str) -> None:
        if id_usuario not in self.ids_usuarios:
            raise UsuarioNoEncontrado("Usuario no encontrado.")
        eliminado = self.usuarios.pop(id_usuario)
        self.ids_usuarios.remove(id_usuario)
        logging.info(f"Usuario dado de baja: {eliminado}")

    def prestar_libro(self, id_usuario: str, isbn: str) -> None:
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontrado("Usuario no registrado.")
        if isbn not in self.libros:
            raise LibroNoDisponible("Libro no disponible en el catálogo.")

        usuario = self.usuarios[id_usuario]
        libro = self.libros.pop(isbn)
        usuario.libros_prestados.append(libro)
        usuario.historial_prestamos.append(libro)
        logging.info(f"'{libro.datos[0]}' prestado a {usuario.nombre}.")

    def devolver_libro(self, id_usuario: str, isbn: str) -> None:
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontrado("Usuario no registrado.")

        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro
                logging.info(f"'{libro.datos[0]}' devuelto por {usuario.nombre}.")
                return
        raise PrestamoInvalido("El usuario no tiene ese libro prestado.")

    def buscar_libros(self, criterio: str, valor: str) -> List[Libro]:
        resultados = []
        for libro in self.libros.values():
            if criterio == "titulo" and valor.lower() in libro.datos[0].lower():
                resultados.append(libro)
            elif criterio == "autor" and valor.lower() in libro.datos[1].lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
                resultados.append(libro)
        logging.info("Resultados encontrados." if resultados else "No se encontraron resultados.")
        return resultados

    def listar_libros_prestados(self, id_usuario: str) -> List[Libro]:
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontrado("Usuario no registrado.")
        return self.usuarios[id_usuario].libros_prestados

    def historial_usuario(self, id_usuario: str) -> List[Libro]:
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontrado("Usuario no registrado.")
        return self.usuarios[id_usuario].historial_prestamos


if __name__ == "__main__":
    biblio = Biblioteca()

    # Libros
    biblio.añadir_libro(Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "111"))
    biblio.añadir_libro(Libro("El Quijote", "Miguel de Cervantes", "Clásico", "222"))
    biblio.añadir_libro(Libro("Python para Todos", "Raúl González", "Programación", "333"))
    biblio.añadir_libro(Libro("1984", "George Orwell", "Distopía", "444"))
    biblio.añadir_libro(Libro("Crónica de una Muerte Anunciada", "Gabriel García Márquez", "Novela", "555"))
    biblio.añadir_libro(Libro("Clean Code", "Robert C. Martin", "Programación", "666"))
    biblio.añadir_libro(Libro("La Odisea", "Homero", "Clásico", "777"))

    # Usuarios
    ana = Usuario("Ana", "U01")
    luis = Usuario("Luis", "U02")
    maria = Usuario("María", "U03")
    carlos = Usuario("Carlos", "U04")
    sofia = Usuario("Sofía", "U05")

    for usuario in [ana, luis, maria, carlos, sofia]:
        biblio.registrar_usuario(usuario)

    # Préstamos
    biblio.prestar_libro("U01", "111")
    biblio.prestar_libro("U01", "222")
    biblio.prestar_libro("U02", "333")
    biblio.prestar_libro("U03", "444")
    biblio.prestar_libro("U04", "555")

    # Consultar libros prestados
    print("Prestados a Ana:", [str(l) for l in biblio.listar_libros_prestados("U01")])
    print("Prestados a Luis:", [str(l) for l in biblio.listar_libros_prestados("U02")])

    # Devoluciones
    biblio.devolver_libro("U01", "111")
    biblio.devolver_libro("U03", "444")

    # Historial de usuarios
    print("Historial de Ana:", [str(l) for l in biblio.historial_usuario("U01")])
    print("Historial de María:", [str(l) for l in biblio.historial_usuario("U03")])

    # Búsquedas
    encontrados = biblio.buscar_libros("categoria", "programación")
    print("Libros encontrados en Programación:", [str(l) for l in encontrados])
