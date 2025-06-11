# Solicita al usuario las temperaturas de los 7 días y las guarda en una lista
def ingresar_temperaturas():
    temp = []
    for dia in range(1, 8):
        t = float(input(f"Ingresar la temperatura del día {dia}: "))
        temp.append(t)
    return temp

# Calcula el promedio de las temperaturas registradas
def calcular_promedio(temps):
    return sum(temps) / len(temps)

# Función principal que coordina el ingreso, cálculo y presentación del promedio
def main_tradicional():
    print("===== INGRESO DE DATOS =====")
    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    print(f"El promedio semanal de la temperatura es: {promedio:.2f}°C")

# Punto de entrada del programa
if __name__ == "__main__":
    main_tradicional()
