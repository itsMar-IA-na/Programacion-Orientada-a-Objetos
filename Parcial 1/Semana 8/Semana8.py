import os
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

HISTORIAL = []

def mostrar_banner():
    print(Fore.CYAN + Style.BRIGHT + """
   ==========================================
        DASHBOARD POO - Mariana López
   ==========================================
    """)

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(Fore.YELLOW + f"\n--- Código de {ruta_script} ---\n")
            print(Fore.WHITE + codigo)
            return codigo
    except FileNotFoundError:
        print(Fore.RED + "El archivo no se encontró.")
        return None
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    HISTORIAL.append(ruta_script)
    try:
        if os.name == 'nt':
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al ejecutar el código: {e}")

def buscar_script(ruta_base, palabra_clave):
    print(Fore.CYAN + f"\nBuscando scripts que contengan '{palabra_clave}'...\n")
    encontrados = []
    for dirpath, _, files in os.walk(ruta_base):
        for f in files:
            if f.endswith(".py") and palabra_clave.lower() in f.lower():
                ruta = os.path.join(dirpath, f)
                encontrados.append(ruta)
    if encontrados:
        for i, ruta in enumerate(encontrados, 1):
            print(f"{i}. {ruta}")
        eleccion = input("\nElige el número para ver el código o ENTER para omitir: ")
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(encontrados):
            mostrar_codigo(encontrados[int(eleccion)-1])
    else:
        print("No se encontraron scripts con esa palabra.")

def mostrar_menu():
    mostrar_banner()
    ruta_base = r"C:\Users\lopez\PycharmProjects\Programacion-Orientada-a-Objetos"

    if not os.path.exists(ruta_base):
        print(Fore.RED + "No se encontró el directorio del proyecto.")
        return

    unidades = [f.name for f in os.scandir(ruta_base) if f.is_dir()]

    while True:
        print(Fore.GREEN + "\nMenu Principal - Unidades POO")
        for i, unidad in enumerate(unidades, 1):
            print(f"{i} - {unidad}")
        print("B - Buscar script por palabra clave")
        print("H - Ver historial de ejecuciones")
        print("0 - Salir")

        eleccion = input("Selecciona una opción: ").strip().lower()
        if eleccion == '0':
            print("Saliendo del programa.")
            break
        elif eleccion == 'b':
            palabra = input("Ingresa la palabra clave: ")
            buscar_script(ruta_base, palabra)
        elif eleccion == 'h':
            print(Fore.CYAN + "\nHistorial de scripts ejecutados:")
            for idx, h in enumerate(HISTORIAL[-5:], 1):
                print(f"{idx}. {h}")
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(unidades):
            mostrar_sub_menu(os.path.join(ruta_base, unidades[int(eleccion)-1]))
        else:
            print("Opción no válida.")

def mostrar_sub_menu(ruta_unidad):
    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print(Fore.BLUE + "\nSubmenú - Selecciona una semana o carpeta")
        for i, carpeta in enumerate(sub_carpetas, 1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar")

        eleccion = input("Elige una subcarpeta: ")
        if eleccion == '0':
            break
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(sub_carpetas):
            mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[int(eleccion)-1]))
        else:
            print("Opción no válida.")

def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    while True:
        print(Fore.MAGENTA + "\nScripts - Ver o ejecutar")
        for i, script in enumerate(scripts, 1):
            print(f"{i} - {script}")
        print("0 - Regresar")

        eleccion = input("Elige un script: ")
        if eleccion == '0':
            break
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(scripts):
            ruta_script = os.path.join(ruta_sub_carpeta, scripts[int(eleccion)-1])
            codigo = mostrar_codigo(ruta_script)
            if codigo:
                ejecutar = input(Fore.GREEN + "¿Deseas ejecutarlo? (1: Sí, 0: No): ")
                if ejecutar == '1':
                    ejecutar_codigo(ruta_script)
                elif ejecutar != '0':
                    print("Opción inválida.")
                input("Presiona Enter para continuar...")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    mostrar_menu()
