from data import temas, guardar_temas_en_archivo

RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"


def crud_preguntas():
    crud_activo = True
    while crud_activo:
        print("\n" + "=" * 40)
        print("        ADMIN - CRUD PREGUNTAS")
        print("=" * 40)
        print("1. Listar preguntas")
        print("2. Crear pregunta")
        print("3. Editar pregunta")
        print("4. Eliminar pregunta")
        print("0. Volver")
        opcion = input(f"\n{GREEN}Elige una opción: {RESET}").strip()

        if opcion == "1":
            listar_preguntas()  
        elif opcion == "2":
            crear_pregunta()
        elif opcion == "3":
            editar_pregunta()
        elif opcion == "4":
            eliminar_pregunta()
        elif opcion == "0":
            crud_activo = False
        else:
            print(f"{RED}Opción inválida.{RESET}")


def seleccionar_tema():
    print(f"\n{YELLOW}--- Seleccionar tema ---{RESET}")
    nombres_temas = list(temas.keys())
    for i, nombre in enumerate(nombres_temas, start=1):
        print(f"{i}. {nombre}")
    opcion = input("Número de tema: ").strip()

    if not opcion.isdigit():
        print(f"{RED}Entrada inválida.{RESET}")
        return None, None, None

    idx = int(opcion) - 1
    if idx < 0 or idx >= len(nombres_temas):
        print(f"{RED}Opción fuera de rango.{RESET}")
        return None, None, None

    tema_seleccionado = nombres_temas[idx]
    return tema_seleccionado, temas[tema_seleccionado], idx


def seleccionar_lista_preguntas():
    tema_nombre, niveles_tema, _ = seleccionar_tema()
    if not tema_nombre:
        return None, None, None

    print(f"\n{YELLOW}--- Elegir dificultad ---{RESET}")
    for i, (nombre_nivel, _) in enumerate(niveles_tema, start=1):
        print(f"{i}. {nombre_nivel}")

    opcion = input("Número de dificultad: ").strip()
    if not opcion.isdigit():
        print(f"{RED}Entrada inválida.{RESET}")
        return None, None, None

    idx = int(opcion) - 1
    if idx < 0 or idx >= len(niveles_tema):
        print(f"{RED}Opción fuera de rango.{RESET}")
        return None, None, None

    nombre_nivel, lista_preguntas = niveles_tema[idx]
    return tema_nombre, nombre_nivel, lista_preguntas


def listar_preguntas(tema=None, nivel=None, lista=None):
    """
    Si no se pasan tema/nivel/lista, se le pide al usuario elegirlos.
    Si se pasan, solo se listan las preguntas de esa lista.
    """
    if tema is None or nivel is None or lista is None:
        tema, nivel, lista = seleccionar_lista_preguntas()
        if not lista:
            return

    print(f"\n{YELLOW}Preguntas de {tema} - {nivel}{RESET}")
    if len(lista) == 0:
        print("No hay preguntas en este nivel.")
        return

    for idx, pregunta in enumerate(lista, start=1):
        correcta = pregunta["correcta"]
        print(
            f"{idx}) {pregunta['texto']} "
            f"(Correcta: {pregunta['opciones'][correcta]})"
        )


def crear_pregunta():
    tema, nivel, lista = seleccionar_lista_preguntas()
    if not lista:
        return

    print(f"\nCreando pregunta en {tema} - {nivel}")
    texto = input(f"{YELLOW}Texto de la pregunta: {RESET}").strip()
    if not texto:
        print(f"{RED}La pregunta no puede estar vacía.{RESET}")
        return

    opciones = []
    print("\nIngresa las 4 opciones de respuesta:")
    for i in range(4):
        op = input(f"  Opción {i + 1}: ").strip()
        if not op:
            print(f"{RED}La opción no puede estar vacía.{RESET}")
            return
        opciones.append(op)

    print("\nHas ingresado estas opciones:")
    for i, op in enumerate(opciones, start=1):
        print(f"  {i}. {op}")

    correcta_str = input(
        "\nEscribe el NÚMERO de la opción correcta (1-4): "
    ).strip()
    if not correcta_str.isdigit():
        print(f"{RED}Entrada inválida. Debes escribir un número del 1 al 4.{RESET}")
        return

    correcta_num = int(correcta_str)
    if correcta_num < 1 or correcta_num > 4:
        print(f"{RED}Número fuera de rango. Debe ser entre 1 y 4.{RESET}")
        return

    correcta_idx = correcta_num - 1

    lista.append({"texto": texto, "opciones": opciones, "correcta": correcta_idx})
    guardar_temas_en_archivo(temas)
    print(f"{GREEN}Pregunta creada en {tema} - {nivel}.{RESET}")


def editar_pregunta():
    tema, nivel, lista = seleccionar_lista_preguntas()
    if not lista or len(lista) == 0:
        print(f"{RED}No hay preguntas para editar en este nivel.{RESET}")
        return

    
    listar_preguntas(tema, nivel, lista)

    idx_str = input(
        "\nEscribe el NÚMERO de la pregunta que quieres editar: "
    ).strip()
    if not idx_str.isdigit():
        print(f"{RED}Entrada inválida. Debes escribir un número.{RESET}")
        return

    num_pregunta = int(idx_str)
    if num_pregunta < 1 or num_pregunta > len(lista):
        print(f"{RED}Número fuera de rango.{RESET}")
        return

    idx = num_pregunta - 1
    pregunta = lista[idx]

    print(f"\nEditando pregunta {num_pregunta} de {tema} - {nivel}")

    nuevo_texto = input(
        f"Nuevo texto (Enter para mantener '{pregunta['texto']}'): "
    ).strip()
    if nuevo_texto:
        pregunta["texto"] = nuevo_texto

    print("\nEdita las opciones (Enter para mantener la actual):")
    for i, op in enumerate(pregunta["opciones"], start=1):
        nueva_op = input(
            f"  Nueva opción {i} (actual: '{op}'): "
        ).strip()
        if nueva_op:
            pregunta["opciones"][i - 1] = nueva_op

    print("\nOpciones actuales:")
    for i, op in enumerate(pregunta["opciones"], start=1):
        marca = " (actualmente correcta)" if (i - 1) == pregunta["correcta"] else ""
        print(f"  {i}. {op}{marca}")

    nueva_correcta = input(
        f"\nNúmero de la opción correcta (1-4, Enter para mantener la actual {pregunta['correcta'] + 1}): "
    ).strip()

    if nueva_correcta:
        if nueva_correcta.isdigit():
            num_correcta = int(nueva_correcta)
            if 1 <= num_correcta <= 4:
                pregunta["correcta"] = num_correcta - 1
            else:
                print(f"{RED}Número fuera de rango, se mantiene la opción correcta anterior.{RESET}")
        else:
            print(f"{RED}Entrada inválida, se mantiene la opción correcta anterior.{RESET}")

    guardar_temas_en_archivo(temas)
    print(f"{GREEN}Pregunta editada y guardada.{RESET}")


def eliminar_pregunta():
    tema, nivel, lista = seleccionar_lista_preguntas()
    if not lista or len(lista) == 0:
        print(f"{RED}No hay preguntas para eliminar en este nivel.{RESET}")
        return

    listar_preguntas(tema, nivel, lista)

    idx_str = input(
        "\nEscribe el NÚMERO de la pregunta que quieres eliminar: "
    ).strip()
    if not idx_str.isdigit():
        print(f"{RED}Entrada inválida. Debes escribir un número.{RESET}")
        return

    num_pregunta = int(idx_str)
    if num_pregunta < 1 or num_pregunta > len(lista):
        print(f"{RED}Número fuera de rango.{RESET}")
        return

    idx = num_pregunta - 1
    pregunta = lista[idx]

    print(f"\nVas a eliminar la pregunta {num_pregunta}:")
    print(f"  {pregunta['texto']}")
    confirm = input("¿Seguro que quieres eliminarla? (s/n): ").strip().lower()
    if confirm == "s":
        lista.pop(idx)
        guardar_temas_en_archivo(temas)
        print(f"{GREEN}Pregunta eliminada de {tema} - {nivel}.{RESET}")
    else:
        print("Operación cancelada.")
