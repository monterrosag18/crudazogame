from utils import leer_contraseña_ocultandola
import json
import os 

archivo_usuarios = "usuarios.json"
usuarios = {}

def cargar_usuarios():
    global usuarios 
    
    if  os.path.exists(archivo_usuarios):

        leer = open(archivo_usuarios, "r", encoding="utf-8")
        contenido = leer.read()
        leer.close()
        usuarios = json.loads(contenido)
    
    else: 
        usuarios = {}

def guardar_usuario():
    contenido = json.dumps(usuarios, ensure_ascii= False, indent = 4)
    escribir = open(archivo_usuarios, "w", encoding="utf-8")
    escribir.write(contenido)
    escribir.close()
    
def registro_usuario():
    nombre = input("Ingrese su nombre de usuario: ").strip()
    if not nombre:
        print("El usuario no puede estar vacío. Ingrese un nombre de usuario. \n")
        return
    if not all(c.isalpha() or c.isdigit() or c.isspace() for c in nombre):
        print("El nombre solo puede contener letras, números y espacios.\n")
        return
    if nombre in usuarios:
        print("Nombre de usuario ya existe. Elija otro nombre de usuario o Inicie sesion.\n")
        return

    contraseña = leer_contraseña_ocultandola("Ingrese una contraseña: ").strip()
    if not contraseña:
        print("La contraseña no puede estar vacía.\n")
        return

    usuarios[nombre] = contraseña
    guardar_usuario()
    print("Usuario registrado con éxito.\n")


def inicio_sesion():
    nombre = input("Ingrese su nombre de usuario: ").strip()
    if not nombre:
        print("El usuario no puede estar vacío. Ingrese un nombre de usuario. \n")
        return None
    if nombre not in usuarios:
        print("Usuario no encontrado.\n")
        return None

    contraseña = leer_contraseña_ocultandola("Ingrese su contraseña: ").strip()
    if usuarios[nombre] == contraseña:
        print("Inicio de sesión exitoso.\n")
        return nombre

    print("Contraseña incorrecta. Vuelva a intentarlo.\n")
    return None

