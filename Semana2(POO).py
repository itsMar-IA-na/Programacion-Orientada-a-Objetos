# Clase que representa un registro diario de temperatura
class RegistroDiario:
    def __init__(self, dia, temperatura):
        self._dia = dia
        self._temperatura = temperatura

    # Encapsulamiento
    @property
    def dia(self):
        return self._dia

    @property
    def temperatura(self):
        return self._temperatura

# Clase que agrupa los registros de una semana
class SemanaClimatica:
    def __init__(self):
        self._registros = []

    def agregar_registro(self, registro: RegistroDiario):
        if len(self._registros) >= 7:
            raise ValueError("Ya se ingresaron 7 días")
        self._registros.append(registro)

    def promedio_semanal(self):
        if not self._registros:
            return 0
        total = sum(r.temperatura for r in self._registros)
        return total / len(self._registros)

    def mostrar_registros(self):
        for r in self._registros:
            print(f"Día {r.dia}: {r.temperatura}°C")

# Función principal
def main_poo():
    semana = SemanaClimatica()
    print("=== INGRESO DE TEMPERATURAS ===")
    for dia in range(1, 8):
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        reg = RegistroDiario(dia, temp)
        semana.agregar_registro(reg)

    print("\n=== RESUMEN SEMANAL ===")
    semana.mostrar_registros()

    promedio = semana.promedio_semanal()
    print(f"\n El promedio semanal de temperatura es: {promedio:.2f}°C")

# Punto de entrada
if __name__ == "__main__":
    main_poo()
