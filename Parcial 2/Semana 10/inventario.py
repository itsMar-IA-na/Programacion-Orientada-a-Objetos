import os
from producto import Producto

class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.productos = []
        self.archivo = archivo
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga los productos desde el archivo, si existe."""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, "r") as f:
                    for linea in f:
                        datos = linea.strip().split(",")
                        if len(datos) == 4:
                            id_p, nombre, cantidad, precio = datos
                            producto = Producto(int(id_p), nombre, int(cantidad), float(precio))
                            self.productos.append(producto)
        except FileNotFoundError:
            print("Archivo no encontrado. Se creará uno nuevo al guardar.")
        except PermissionError:
            print("Error: No tiene permisos para acceder al archivo.")
        except Exception as e:
            print(f"Error inesperado al cargar inventario: {e}")

    def guardar_en_archivo(self):
        """Guarda todos los productos en el archivo."""
        try:
            with open(self.archivo, "w") as f:
                for p in self.productos:
                    f.write(f"{p.id_producto},{p.nombre},{p.cantidad},{p.precio}\n")
        except PermissionError:
            print("Error: No tiene permisos para guardar el archivo.")
        except Exception as e:
            print(f"Error inesperado al guardar inventario: {e}")

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_en_archivo()
        print(f"Producto '{producto.nombre}' agregado y guardado en el archivo.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.id_producto == id_producto:
                self.productos.remove(p)
                self.guardar_en_archivo()
                print(f"Producto con ID {id_producto} eliminado del archivo.")
                return
        print(f"Producto con ID {id_producto} no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for p in self.productos:
            if p.id_producto == id_producto:
                if cantidad is not None:
                    p.cantidad = cantidad
                if precio is not None:
                    p.precio = precio
                self.guardar_en_archivo()
                print(f"Producto con ID {id_producto} actualizado en el archivo.")
                return
        print(f"Producto con ID {id_producto} no encontrado.")

    def buscar_producto_por_nombre(self, nombre):
        encontrados = [p for p in self.productos if p.nombre.lower() == nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print(f"No se encontraron productos con el nombre '{nombre}'.")

    def mostrar_inventario(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("\nInventario completo:")
            for p in self.productos:
                print(p)
