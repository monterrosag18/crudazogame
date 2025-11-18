from utils import validar_entero_menu
from auth import registro_usuario, inicio_sesion, cargar_usuarios
from game import jugar
from administrador_crud import crud_preguntas


ADMINS = {"dani"}


def menu_principal():
    menu = (
        "\n--- PinguiMundo ---\n"
        "1. Registrar nuevo usuario\n"
        "2. Iniciar sesión\n"
        "3. Salir\n"
    )
    return validar_entero_menu(menu, "Seleccione una opción (1-3): ", 1, 3)


def main():
    cargar_usuarios()
    main_iniciado = True
    sesion = None
    while main_iniciado:
        if sesion is None:
            opcion = menu_principal()

            match opcion:
                case 1:
                    registro_usuario()
                case 2:
                    sesion = inicio_sesion()
                case 3:
                    main_iniciado = False
                    print("Fin del juego. ¡Vuelve pronto!")
        else:
            if sesion in ADMINS:
                menu_admin = (
                    "\n--- Menú Administrador ---\n"
                    "1. Administrar preguntas\n"
                    "2. Jugar\n"
                    "3. Cerrar sesión\n"
                    "4. Salir\n"
                )
                opcion_admin = validar_entero_menu(
                    menu_admin,
                    "Seleccione una opción (1-4): ",
                    1,
                    4,
                )

                if opcion_admin == 1:
                    crud_preguntas()
                elif opcion_admin == 2:
                    resultado = jugar(sesion)
                    if resultado == "cambiar_usuario":
                        sesion = None
                    elif resultado == "salir":
                        print("Fin del juego. ¡Vuelve pronto!")
                        main_iniciado = False
                elif opcion_admin == 3:
                    sesion = None
                elif opcion_admin == 4:
                    print("Fin del juego. ¡Vuelve pronto!")
                    main_iniciado = False
            else:
                resultado = jugar(sesion)

                if resultado == "cambiar_usuario":
                    sesion = None

                elif resultado == "salir":
                    print("Fin del juego. ¡Vuelve pronto!")
                    main_iniciado = False


main()
