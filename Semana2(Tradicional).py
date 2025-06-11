def ingresar_temperaturas():
    temp = []
    for dia in range(1, 8):
        t = float(input(f"Ingresar la temperatura del día {dia}: "))
        temp.append(t)
    return temp

def calcular_promedio(temps):
    return sum(temps) / len(temps)

def main_tradicional():
    print("===== INGRESO DE DATOS =====")
    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    print(f"El promedio semanal de la temperatura es: {promedio:.2f}°C")

if __name__ == "__main__":
    main_tradicional()
