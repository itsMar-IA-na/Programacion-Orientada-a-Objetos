class RegistroDiario:
    def __init__(self, dia, temp):
        self._dia = dia
        self._temperatura = temp

    @property
    def temperatura(self):
        return self._temperatura

    @property
    def dia(self):
        return self._dia

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
        total = sum(reg.temperatura for reg in self._registros)
        return total / len(self._registros)

def main_poo():
    semana = SemanaClimatica()
    print("=== INGRESO DE DATOS ===")
    for dia in range(1, 8):
        t = float(input(f"Ingrese la temperatura del día {dia}: "))
        reg = RegistroDiario(dia, t)
        semana.agregar_registro(reg)

    prom = semana.promedio_semanal()
    print(f"La temperatura promedio de la semana es: {prom:.2f}°C")

if __name__ == "__main__":
    main_poo()
#END