# Programa: Conversor de Temperaturas (En relación a los temas tratados en Física)
# Objetivo: Resolver ejercicios de conversión de unidades de temperatura de manera rápida y efectiva.
# Descripción: Este programa permite al usuario ingresar una temperatura en Celsius, Fahrenheit o Kelvin.
# Luego convierte esa temperatura a las otras dos escalas y clasifica el estado térmico (fría, templada o caliente)
# en función de su valor equivalente en grados Celsius.

def convertir_a_celsius(valor, unidad_origen):
    "Convierte la temperatura de Fahrenheit o Kelvin a Celsius."
    if unidad_origen == "fahrenheit":
        return (valor - 32) * 5/9
    elif unidad_origen == "kelvin":
        return valor - 273.15
    return valor  # Si ya está en celsius


def convertir_desde_celsius(celsius):
    "Convierte grados Celsius a Fahrenheit y Kelvin."
    fahrenheit = (celsius * 9/5) + 32
    kelvin = celsius + 273.15
    return fahrenheit, kelvin


def clasificar_temperatura(celsius):
    "Clasifica la temperatura como fría, templada o caliente según grados Celsius."
    if celsius < 10:
        return "Fría"
    elif 10 <= celsius <= 25:
        return "Templada"
    else:
        return "Caliente"


# Solicitar al usuario la unidad de entrada
print("Conversor de Temperaturas")
print("Unidades disponibles: celsius, fahrenheit, kelvin")
unidad = input("Ingrese la unidad de la temperatura que va a ingresar: ").strip().lower()

# Validar la unidad ingresada
if unidad not in ["celsius", "fahrenheit", "kelvin"]:
    print("Unidad no válida. Por favor, ingrese: celsius, fahrenheit o kelvin.")
else:
    # Solicitar el valor numérico
    valor_temperatura = float(input(f"Ingrese el valor de la temperatura en {unidad}: "))

    # Convertir a Celsius
    temperatura_celsius = convertir_a_celsius(valor_temperatura, unidad)

    # Convertir a otras escalas
    temperatura_fahrenheit, temperatura_kelvin = convertir_desde_celsius(temperatura_celsius)

    # Clasificar temperatura
    estado_termico = clasificar_temperatura(temperatura_celsius)

    # Mostrar resultados
    print("\n--- Resultados ---")
    print(f"Temperatura en Celsius: {temperatura_celsius:.2f} °C")
    print(f"Temperatura en Fahrenheit: {temperatura_fahrenheit:.2f} °F")
    print(f"Temperatura en Kelvin: {temperatura_kelvin:.2f} K")
    print(f"Clasificación: {estado_termico}")
