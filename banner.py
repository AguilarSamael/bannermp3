import os
import subprocess

def instalar_mpv():
    try:
        subprocess.run(["mpv", "--version"])
    except FileNotFoundError:
        print("Instalando mpv...")
        os.system("pkg install mpv -y")

def instalar_figlet():
    try:
        subprocess.run(["figlet", "--version"])
    except FileNotFoundError:
        print("Instalando figlet...")
        os.system("pkg install figlet -y")

def instalar_lolcat():
    try:
        subprocess.run(["lolcat", "--version"])
    except FileNotFoundError:
        print("Instalando lolcat...")
        os.system("pkg install lolcat -y")

def guardar_configuracion(texto, ruta_cancion):
    with open("/data/data/com.termux/files/home/.banner_config", "w") as f:
        f.write(f"texto={texto}\n")
        f.write(f"ruta_cancion={ruta_cancion}\n")

def cargar_configuracion():
    try:
        with open("/data/data/com.termux/files/home/.banner_config", "r") as f:
            configuracion = {}
            for linea in f.readlines():
                clave, valor = linea.strip().split("=")
                configuracion[clave] = valor
            return configuracion
    except FileNotFoundError:
        return None

def agregar_a_bashrc():
    ruta_script = os.path.abspath(__file__)
    with open("/data/data/com.termux/files/home/.bashrc", "r+") as f:
        lines = f.readlines()
        if f"python {ruta_script}" not in [line.strip() for line in lines]:
            f.write(f"python {ruta_script}\n")

def borrar_configuracion():
    try:
        os.remove("/data/data/com.termux/files/home/.banner_config")
        print("Configuración borrada con éxito.")
    except FileNotFoundError:
        print("No existe una configuración guardada.")

def modificar_configuracion():
    configuracion = cargar_configuracion()
    if configuracion:
        texto = input(f"Ingrese el nuevo texto para el banner ({configuracion['texto']}): ")
        if texto == "":
            texto = configuracion["texto"]
        ruta_cancion = input(f"Ingrese la nueva ruta de la canción ({configuracion['ruta_cancion']}): ")
        if ruta_cancion == "":
            ruta_cancion = configuracion["ruta_cancion"]
        guardar_configuracion(texto, ruta_cancion)
        print("Configuración modificada con éxito.")
    else:
        print("No existe una configuración guardada.")

def crear_banner():
    instalar_mpv()
    instalar_figlet()
    instalar_lolcat()
    configuracion = cargar_configuracion()
    if configuracion:
        texto = configuracion["texto"]
        ruta_cancion = configuracion["ruta_cancion"]
    else:
        texto = input("Ingrese el texto para el banner: ")
        ruta_cancion = input("Ingrese la ruta de la canción: ")
        guardar_configuracion(texto, ruta_cancion)
        agregar_a_bashrc()
        print("¡Listo! El banner se mostrará cada vez que abras Termux.")
    # Mostrar el banner con letras grandes
    os.system("clear")
    os.system(f"figlet -f standard '{texto}' | lolcat -F 0.5")
    # Reproducir solo 30 segundos de la canción
    subprocess.run(["mpv", "--start=0", "--length=30", ruta_cancion])

def main():
    configuracion = cargar_configuracion()
    while True:
        if configuracion:
            print("1. Mostrar banner")
            print("2. Borrar configuración")
            print("3. Modificar configuración")
            print("4. Salir")
            opcion = input("Ingrese su opción: ")
            if opcion == "1":
                crear_banner()
            elif opcion == "2":
                borrar_configuracion()
                configuracion = None
            elif opcion == "3":
                modificar_configuracion()
                configuracion = cargar_configuracion()
            elif opcion == "4":
                print("Saliendo...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
        else:
            crear_banner()
            configuracion = cargar_configuracion()

if __name__ == "__main__":
    main()