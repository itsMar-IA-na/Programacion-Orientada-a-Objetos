class Insecto:
    def __init__(self, nombre, alas, patas, energia):
        self.nombre = nombre
        self.alas = alas
        self.patas = patas
        self.energia = energia

    def mostrar_datos(self):
        print(f"Insecto: {self.nombre}")
        print(f"-Alas: {self.alas}")
        print(f"-Patas: {self.patas}")
        print(f"-Energía: {self.energia}")

    def esta_activo(self):
        return self.energia > 0

    def descansar(self):
        self.energia += 10
        print(f"La {self.nombre} ha descansado, así que su energía actual es: {self.energia}")

    # Metodo polimórfico
    def moverse(self):
        pass

# HERENCIA + POLIMORFISMO
class Abeja(Insecto):
    def __init__(self, nombre, energia, tipo_miel):
        super().__init__(nombre, alas=4, patas=6, energia=energia)
        self.tipo_miel = tipo_miel

    def moverse(self):
        if self.energia >= 5:
            self.energia -= 5
            print(f"La {self.nombre} vuela recolectando polen.")
        else:
            print(f"La {self.nombre} está muy cansada para volar.")

    def producir_miel(self):
        if self.energia >= 10:
            print(f"La {self.nombre} ha producido miel de tipo {self.tipo_miel}.")
            self.energia -= 10
        else:
            print(f"La {self.nombre} no tiene suficiente energía para producir miel.")


class Hormiga(Insecto):
    def __init__(self, nombre, energia, tipo_trabajo):
        super().__init__(nombre, alas=0, patas=6, energia=energia)
        self.tipo_trabajo = tipo_trabajo

    def moverse(self):
        if self.energia >= 3:
            self.energia -= 3
            print(f"La {self.nombre} trabaja transportando hojas.")
        else:
            print(f"La {self.nombre} está muy cansada para moverse.")

    def trabajar(self):
        print(f"La {self.nombre} realiza tareas de tipo {self.tipo_trabajo}.")


# FUNCIÓN DE SIMULACIÓN DE ECOSISTEMA
def ecosistema(insecto_1, insecto_2):
    print("\n Inicia actividad en el ecosistema...\n")
    turnos = 3
    for turno in range(1, turnos + 1):
        print(f"--- Turno {turno} ---")
        insecto_1.moverse()
        insecto_2.moverse()
        insecto_1.descansar()
        insecto_2.descansar()
        print()

    print(" Fin de la actividad.\n")
    insecto_1.mostrar_datos()
    insecto_2.mostrar_datos()


# CREACIÓN DE OBJETOS CON NOMBRES NUEVOS
maya = Abeja(nombre=" Abeja Maya", energia=20, tipo_miel="Miel de flores")
doti = Hormiga(nombre="Hormiga Doti", energia=15, tipo_trabajo="Construcción")

# EJECUCIÓN
maya.mostrar_datos()
print()
doti.mostrar_datos()
print()

ecosistema(maya, doti)
#Fin