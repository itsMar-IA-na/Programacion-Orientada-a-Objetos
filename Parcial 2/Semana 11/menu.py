from inventario import Inventario
from producto import Producto

def menu():
    inventario = Inventario()

    while True:
        print("\n===== Sistema de Inventario de Libros =====")
        print("1. Agregar libro")
        print("2. Eliminar libro")
        print("3. Actualizar libro")
        print("4. Buscar libro por nombre")
        print("5. Mostrar inventario completo")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_p = int(input("Ingrese el ID del libro: "))
                nombre = input("Ingrese el nombre del libro: ")
                cantidad = int(input("Ingrese la cantidad disponible: "))
                precio = float(input("Ingrese el precio: "))
                nuevo = Producto(id_p, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo)
            except ValueError:
                print("Error: datos inválidos. Intente nuevamente.")

        elif opcion == "2":
            try:
                id_p = int(input("Ingrese el ID del libro a eliminar: "))
                inventario.eliminar_producto(id_p)
            except ValueError:
                print("Error: ID inválido.")

        elif opcion == "3":
            try:
                id_p = int(input("Ingrese el ID del libro a actualizar: "))
                cantidad = input("Nueva cantidad (Enter para no cambiar): ")
                precio = input("Nuevo precio (Enter para no cambiar): ")

                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None

                inventario.actualizar_producto(id_p, cantidad, precio)
            except ValueError:
                print("Error: datos inválidos.")

        elif opcion == "4":
            nombre = input("Ingrese el nombre a buscar: ")
            inventario.buscar_producto_por_nombre(nombre)

        elif opcion == "5":
            inventario.mostrar_inventario()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    menu()
