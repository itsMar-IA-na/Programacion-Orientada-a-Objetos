class Planta:

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.altura = 0  # en centímetros
        print(f"Se ha plantado un {self.tipo} llamad@ '{self.nombre}'.")

    def regar(self):
        self.altura += 5
        print(f"Se ha regado a '{self.nombre}'. Ahora mide {self.altura} cm.")

    def fumigar(self):
        print(f"Has fumigado a '{self.nombre}' para protegerla de plagas.")

    def __del__(self):
        print(f"La planta '{self.nombre}' fue cocechada del jardín.")


# Simulación de uso
def main():
    mi_planta = Planta("Margarita", "Girasol")
    mi_planta.regar()
    mi_planta.regar()
    mi_planta.fumigar()
    # El destructor se invocará automáticamente al finalizar el programa o cuando el objeto ya no sea referenciado.


if __name__ == "__main__":
    main()

