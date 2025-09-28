import random
import time

# Simulación de memoria con bloques fijos (simula la memoria física)
class Memoria:
    def __init__(self, tamanio):
        self.tamanio = tamanio
        self.memoria = [None] * tamanio  # Lista que representa los bloques de memoria

    # Método para intentar asignar memoria
    def asignar(self, proceso, tamanio_requerido):
        for i in range(self.tamanio - tamanio_requerido + 1):
            # Buscar un bloque contiguo libre
            if all(self.memoria[i + j] is None for j in range(tamanio_requerido)):
                # Asignar el bloque de memoria
                for j in range(tamanio_requerido):
                    self.memoria[i + j] = proceso
                print(f"Proceso {proceso} asignó {tamanio_requerido} bloques de memoria.")
                return True
        print(f"Proceso {proceso} no pudo asignar memoria. No hay suficiente espacio contiguo.")
        return False

    # Método para liberar memoria
    def liberar(self, proceso):
        for i in range(self.tamanio):
            if self.memoria[i] == proceso:
                self.memoria[i] = None
        print(f"Proceso {proceso} ha liberado su memoria.")

    # Método para mostrar el estado de la memoria
    def mostrar_memoria(self):
        print("Estado actual de la memoria:")
        print(self.memoria)

# Simulación de un proceso que pide memoria y luego la libera
def proceso(nombre, memoria):
    tamanio_requerido = random.randint(1, 5)  # Cantidad aleatoria de bloques de memoria
    print(f"{nombre} está pidiendo {tamanio_requerido} bloques de memoria.")
    if memoria.asignar(nombre, tamanio_requerido):
        time.sleep(random.randint(1, 3))  # El proceso realiza una tarea
        memoria.liberar(nombre)  # Liberamos la memoria
        time.sleep(random.randint(1, 2))  # Simulamos tiempo entre los procesos

# Función para simular la gestión de memoria
def gestionar_memoria():
    memoria = Memoria(10)  # Crear una memoria de tamaño 10 bloques
    procesos = ['Proceso-A', 'Proceso-B', 'Proceso-C', 'Proceso-D', 'Proceso-E']
    for i in range(5):
        proceso_nombre = random.choice(procesos)  # Elegir un proceso al azar
        proceso(proceso_nombre, memoria)  # Ejecutar el proceso
        memoria.mostrar_memoria()  # Mostrar el estado final de la memoria

# Ejecución de la simulación
if __name__ == "__main__":
    gestionar_memoria()

