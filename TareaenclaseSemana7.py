class Vehiculo:
    def __init__(self, placa):
        self.placa = placa
        self._registrar_ingreso()

    def _registrar_ingreso(self):
        print(f"Vehículo con placa {self.placa} ha ingresado al parqueadero.")

    def __del__(self):
        self._registrar_salida()

    def _registrar_salida(self):
        print(f" Vehículo con placa {self.placa} ha salido del parqueadero.")


def simular_parqueadero():
    print(">>> Iniciando simulación del parqueadero...\n")

    def ciclo_de_vida():
        vehiculo1 = Vehiculo("MAR-123")
        vehiculo2 = Vehiculo("ISA-456")
        print("\n>>> Vehículos estacionados.\n")

    ciclo_de_vida()

    print("\n>>> Simulación finalizada.")


if __name__ == "__main__":
    simular_parqueadero()

