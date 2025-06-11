# Clase que representa una mascota
class Mascota:
    def __init__(self, nombre, especie, raza, edad):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.historial = []

    def agregar_historial(self, descripcion):
        self.historial.append(descripcion)

    def mostrar_historial(self):
        print(f"\nHistorial médico de {self.nombre} ({self.especie}, raza {self.raza}, {self.edad} años):")
        for entrada in self.historial:
            print(f"- {entrada}")

# Clase que representa la clínica veterinaria
class ClinicaVeterinaria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pacientes = []

    def registrar_mascota(self, mascota):
        self.pacientes.append(mascota)
        print(f"Mascota registrada: {mascota.nombre} ({mascota.especie}, {mascota.raza})")

    def mostrar_mascotas(self):
        print("\nListado de mascotas registradas:")
        for m in self.pacientes:
            print(f"{m.nombre} - {m.especie} ({m.raza}), {m.edad} años")

# Crear clínica y mascotas con raza incluida
clinica = ClinicaVeterinaria("Veterinaria Mariana")
m1 = Mascota("Maya", "Perro", "Pekinés", 8)
m2 = Mascota("Fresita", "Gato", "Maine Coon", 5)

# Registro e historial
clinica.registrar_mascota(m1)
clinica.registrar_mascota(m2)

clinica.mostrar_mascotas()

# Agregar historial médico a Maya
m1.agregar_historial("Can con todas sus vacunas")
m1.agregar_historial("No presenta historial de enfermedades previas")
m1.agregar_historial("Cirugía previa: Esterilización")
m1.agregar_historial("No presenta historial de problemas de salud crónicos")
m1.agregar_historial("No se le está administrando ningún medicamento")
m1.agregar_historial("No tiene alergias")
m1.agregar_historial("No presenta ansiedad ni agresividad")

# Mostrar historial
m1.mostrar_historial()

m2.agregar_historial("Gato no presenta todas sus vacunas")
m2.agregar_historial("No presenta historial de enfermedades previas")
m2.agregar_historial("Sin cirugía previa")
m2.agregar_historial("Presenta historial de problemas de salud crónicos: enfermedad renal crónica")
m2.agregar_historial("Se le está administrando medicamento: Inhibidores de la ECA y antihipertensivos")
m2.agregar_historial("No tiene alergias")
m2.agregar_historial("No presenta ansiedad ni agresividad")

# Mostrar historial
m2.mostrar_historial()