# Clase base: Persona
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}"


# Clase derivada: Estudiante
class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera, promedio):
        super().__init__(nombre, edad)
        self.carrera = carrera
        self.__promedio = promedio  # Encapsulación (atributo privado)

    # Getter
    def obtener_promedio(self):
        return self.__promedio

    # Setter
    def actualizar_promedio(self, nuevo_promedio):
        if 0 <= nuevo_promedio <= 10:
            self.__promedio = nuevo_promedio
        else:
            print("Promedio inválido. Debe estar entre 0 y 10.")

    # Polimorfismo
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base}, Carrera: {self.carrera}, Promedio: {self.__promedio}"


# Clase derivada: Profesor
class Profesor(Persona):
    def __init__(self, nombre, edad, asignatura, salario):
        super().__init__(nombre, edad)
        self.asignatura = asignatura
        self.__salario = salario  # Encapsulado

    # Getter
    def obtener_salario(self):
        return self.__salario

    # Setter
    def actualizar_salario(self, nuevo_salario):
        if nuevo_salario > 0:
            self.__salario = nuevo_salario
        else:
            print("El salario debe ser positivo.")

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base}, Asignatura: {self.asignatura}, Salario: ${self.__salario}"


# Clase derivada: Administrativo
class Administrativo(Persona):
    def __init__(self, nombre, edad, departamento):
        super().__init__(nombre, edad)
        self.departamento = departamento

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base}, Departamento: {self.departamento}"


# Bloque principal para probar el código
if __name__ == "__main__":
    estudiante1 = Estudiante("Mariana", 19, "Ingeniería en Tecnologías de Información", 9.3)
    profesor1 = Profesor("Rubén", 33, "Metodología de la Investigación", 1250)
    admin1 = Administrativo("Carla", 37, "RRHH")

    print("----- Información Estudiante -----")
    print(estudiante1.mostrar_info())
    estudiante1.actualizar_promedio(9.5)
    print("Promedio actualizado:", estudiante1.obtener_promedio())

    print("\n----- Información Profesor -----")
    print(profesor1.mostrar_info())
    profesor1.actualizar_salario(1300)
    print("Salario actualizado:", profesor1.obtener_salario())

    print("\n----- Información Administrativo -----")
    print(admin1.mostrar_info())

