import pwinput

def leer_contraseña_ocultandola(entrada):
    contraseña = pwinput.pwinput(entrada, mask = "•")
    return contraseña


def validar_entero_menu(menu_texto, mensaje, minimo=None, maximo=None):
    while True:
        print(menu_texto)
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo or maximo is not None and valor > maximo:
                raise ValueError
            return valor
        except ValueError:
            print("Opción inválida. Ingrese un valor disponible en el menú.\n")