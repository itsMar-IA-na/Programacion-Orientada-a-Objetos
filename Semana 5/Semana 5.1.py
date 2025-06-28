# Programa: Conversor de Temperaturas (En relación a los temas tratados en Física)
# Objetivo: Resolver ejercicios de conversión de unidades de temperatura de manera rápida y efectiva.
# Descripción: Permite al usuario ingresar una temperatura en Celsius, Fahrenheit o Kelvin
# (indicando solo una letra: c, f o k). Luego convierte esa temperatura a las otras dos escalas y clasifica
# el estado térmico como frío, templado o caliente, en base a su valor en grados Celsius.

def convertir_a_celsius(valor, unidad_origen):
    "Convierte la temperatura desde Fahrenheit o Kelvin a Celsius."
    if unidad_origen == "f":
        return (valor - 32) * 5 / 9
    elif unidad_origen == "k":
        return valor - 273.15
    return valor  # Ya está en Celsius


def convertir_desde_celsius(celsius):
    "Convierte grados Celsius a Fahrenheit y Kelvin."
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15
    return fahrenheit, kelvin


def clasificar_temperatura(celsius):
    "Clasifica la temperatura como fría, templada o caliente según su valor en °C."
    if celsius < 10:
        return "Fría"
    elif 10 <= celsius <= 25:
        return "Templada"
    else:
        return "Caliente"


# Solicitar al usuario la unidad de entrada
print("Conversor de Temperaturas")
print("Unidades disponibles: c (Celsius), f (Fahrenheit), k (Kelvin)")
unidad = input("Ingrese la unidad de la temperatura (c, f o k): ").strip().lower()

# Validar la unidad ingresada
if unidad not in ["c", "f", "k"]:
    print("Unidad no válida. Por favor, ingrese 'c', 'f' o 'k'.")
else:
    # Solicitar el valor numérico de la temperatura
    valor_temperatura = float(input("Ingrese el valor de la temperatura: "))

    # Convertir a Celsius
    temperatura_celsius = convertir_a_celsius(valor_temperatura, unidad)

    # Obtener conversiones
    temperatura_fahrenheit, temperatura_kelvin = convertir_desde_celsius(temperatura_celsius)

    # Clasificación térmica
    estado_termico = clasificar_temperatura(temperatura_celsius)

    # Mostrar resultados
    print("\n---- Resultados ----")
    print(f"Temperatura en Celsius: {temperatura_celsius:.2f} °C")
    print(f"Temperatura en Fahrenheit: {temperatura_fahrenheit:.2f} °F")
    print(f"Temperatura en Kelvin: {temperatura_kelvin:.2f} K")
    print(f"Clasificación: {estado_termico}")
