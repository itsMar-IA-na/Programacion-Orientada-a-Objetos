from producto import Producto

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar_producto(self, producto: Producto):
        if producto.id_producto in self.productos:
            print(f"El producto con ID {producto.id_producto} ya existe.")
        else:
            self.productos[producto.id_producto] = producto
            print(f"Producto '{producto.nombre}' agregado correctamente.")

    def eliminar_producto(self, id_producto: int):
        if id_producto in self.productos:
            eliminado = self.productos.pop(id_producto)
            print(f"Producto '{eliminado.nombre}' eliminado.")
        else:
            print(f"No se encontró un producto con ID {id_producto}.")

    def actualizar_producto(self, id_producto: int, cantidad: int = None, precio: float = None):
        if id_producto in self.productos:
            self.productos[id_producto].actualizar(cantidad, precio)
            print(f"Producto '{self.productos[id_producto].nombre}' actualizado correctamente.")
        else:
            print(f"No se encontró un producto con ID {id_producto}.")

    def buscar_producto_por_nombre(self, nombre: str):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            for producto in encontrados:
                print(producto)
        else:
            print(f"No se encontraron productos con el nombre '{nombre}'.")

    def mostrar_inventario(self):
        if self.productos:
            print("\nInventario actual:")
            for producto in self.productos.values():
                print(producto)
        else:
            print("El inventario está vacío.")
