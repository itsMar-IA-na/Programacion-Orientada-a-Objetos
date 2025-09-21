class Producto:
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def actualizar(self, cantidad: int = None, precio: float = None):
        """Actualiza la cantidad y/o el precio del producto."""
        if cantidad is not None:
            self.cantidad = cantidad
        if precio is not None:
            self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"
