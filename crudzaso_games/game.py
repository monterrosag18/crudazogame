import curses
from sounds import (
    sonido_tiempo_tick,
    sonido_correcta,
    sonido_incorrecta,
    sonido_bonus
)

import random
from data import temas
from utils import validar_entero_menu
import time
import winsound
import sys


RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def seleccionar_tema():
    menu = ("\n---Seleccione un tema para comenzar a jugar---\n"
            "1. Cultura\n2. Ingles\n3. Historia\n4. Python\n5. Musica y Arte\n")
    opcion = validar_entero_menu(menu, "Elija una opcion de juego (1-5):", 1,5)
    
    match opcion:
        case 1:
            return "Cultura"
        case 2: 
            return "Ingles"
        case 3:
            return "Historia"
        case 4:
            return "Python"
        case 5: 
            return "Musica"
        
def seleccionar_modo():
    menu = ("\n---Selecciona modo de juego---\n"
            "1. Normal (Sin limite de tiempo)\n2. Modo contrareloj(10 segundos por pregunta)\n")
    opcion = validar_entero_menu(menu, "Elija un modo de juego(1-2:)",1,2)
    match opcion:
        case 1:
            return False, 0
        case 2:
            return True, 10

def seleccionar_dificultad_y_cantidad(tema):
    niveles_tema = temas[tema]
    
    menu=("\n---Seleccione dificultad---\n")
    for i, (nombre_nivel, _) in enumerate(niveles_tema, start= 1):
        menu += f"{i}.{nombre_nivel}\n"
    opcion_mezcla = len(niveles_tema) +1
    menu += f"{opcion_mezcla}. Mezclar todas las dificultades\n"
    
    opcion = validar_entero_menu(
        menu, "Elija una dificultad: ",
        1,
        opcion_mezcla
    )
    
    if opcion == opcion_mezcla:
        nombre_nivel = "Mixto"
        preguntas = []
        for _, lista in niveles_tema:
            preguntas.extend(lista)
    else:
        nombre_nivel, preguntas = niveles_tema[opcion - 1]
        
    max_preg = len(preguntas)
    menu_cant = (
        f"\nHay {max_preg} preguntas disponibles en este modo.\n"
        "¿Cuántas quieres responder?\n"
    )
    cantidad = validar_entero_menu(
        menu_cant,
        f"Elige una cantidad (1-{max_preg}): ",
        1,
        max_preg
    )
    
    preguntas_seleccionadas = random.sample(preguntas, cantidad)
    return [(nombre_nivel, preguntas_seleccionadas)]
        
def inicializar_colores():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_CYAN, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_YELLOW, -1)
    curses.init_pair(7, curses.COLOR_GREEN, -1)
    curses.init_pair(8, curses.COLOR_RED, -1)
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK) 
    
def obtener_limite_por_nivel(nombre_nivel):
    nombre = nombre_nivel.lower()

    if "fácil" in nombre or "facil" in nombre:
        return 10   
    elif "intermedio" in nombre or "medio" in nombre:
        return 20
    elif "difícil" in nombre or "dificil" in nombre:
        return 30
    else:
        return 15
    
def obtener_multiplicador_puntaje(nombre_nivel):
    nombre = nombre_nivel.lower()
    if "fácil" in nombre or "facil" in nombre:
        return 1
    elif "intermedio" in nombre or "medio" in nombre:
        return 2
    elif "difícil" in nombre or "dificil" in nombre:
        return 3
    else:
        return 2
    
    
def seleccionar_pregunta(pregunta):
    texto = pregunta["texto"]
    opciones = pregunta["opciones"].copy()
    correcta = opciones[pregunta["correcta"]]
    random.shuffle(opciones)
    indice_correcta = opciones.index(correcta)
    return texto, opciones, indice_correcta


def seleccionar_opcion(stdscr, header, texto, opciones):
    curses.curs_set(0)
    posicion_seleccion = 0
    continuar = True

    while continuar:
        h, w = stdscr.getmaxyx()
        stdscr.clear()

        header_recortado = header[: max(0, w - 1)]
        texto_recortado = texto[: max(0, w - 1)]

        stdscr.addstr(0, 0, header_recortado, curses.color_pair(6))
        if h > 2:
            stdscr.addstr(2, 0, texto_recortado, curses.color_pair(4))

        for i, opcion in enumerate(opciones):
            fila = i + 4
            if fila >= h - 1:
                break

            prefijo = "> " if i == posicion_seleccion else "  "
            texto_op = prefijo + str(opcion)

            if len(texto_op) > w - 1:
                if w > 4:
                    texto_op = texto_op[: w - 4] + "..."
                else:
                    texto_op = texto_op[: max(0, w - 1)]

            if i == posicion_seleccion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(fila, 0, texto_op)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(fila, 0, texto_op)

        stdscr.refresh()

        tecla_presionada = stdscr.getch()

        if tecla_presionada == curses.KEY_UP and posicion_seleccion > 0:
            posicion_seleccion -= 1
        elif tecla_presionada == curses.KEY_DOWN and posicion_seleccion < len(opciones) - 1:
            posicion_seleccion += 1
        elif tecla_presionada in (curses.KEY_ENTER, 10, 13):
            continuar = False

    return posicion_seleccion


def seleccion_opcion_temporizado(stdscr, header, texto, opciones, limite_segundos):
    curses.curs_set(0)
    stdscr.nodelay(True)

    posicion_seleccion = 0
    continuar = True
    seleccion = None
    tiempo_agotado = False

    inicio = time.time()
    ultimo_segundo = limite_segundos

    while continuar:
        h, w = stdscr.getmaxyx()
        stdscr.clear()

        header_recortado = header[: max(0, w - 1)]
        texto_recortado = texto[: max(0, w - 1)]

        stdscr.addstr(0, 0, header_recortado, curses.color_pair(6))
        if h > 2:
            stdscr.addstr(2, 0, texto_recortado, curses.color_pair(4))

        transcurrido = time.time() - inicio
        restante = int(limite_segundos - transcurrido)
        if restante < 0:
            restante = 0

        if restante != ultimo_segundo:
            if restante > 0:
                sonido_tiempo_tick()
            ultimo_segundo = restante

        if transcurrido >= limite_segundos:
            tiempo_agotado = True
            continuar = False

        for i, opcion in enumerate(opciones):
            fila = i + 4
            if fila >= h - 3:
                break

            prefijo = "> " if i == posicion_seleccion else "  "
            texto_op = prefijo + str(opcion)

            if len(texto_op) > w - 1:
                if w > 4:
                    texto_op = texto_op[: w - 4] + "..."
                else:
                    texto_op = texto_op[: max(0, w - 1)]

            if i == posicion_seleccion:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(fila, 0, texto_op)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(fila, 0, texto_op)

        timer_fila = len(opciones) + 6
        if timer_fila >= h - 2:
            timer_fila = max(0, h - 3)

        ancho_timer = min(20, max(5, w - 2))

        fraccion = restante / limite_segundos if limite_segundos > 0 else 0
        fraccion = max(0, min(1, fraccion))

        rellenos = int(ancho_timer * fraccion)
        vacios = ancho_timer - rellenos

        barra = ("▉" * rellenos + "-" * vacios)[: max(0, w - 1)]

        if fraccion > 0.66:
            color_barra = curses.color_pair(7)
        elif fraccion > 0.33:
            color_barra = curses.color_pair(8)
        else:
            color_barra = curses.color_pair(9)

        stdscr.attron(color_barra)
        stdscr.addstr(timer_fila, 0, barra)
        stdscr.attroff(color_barra)

        if timer_fila + 1 < h:
            linea_tiempo = f"Tiempo restante: {int(restante)} segundos"
            stdscr.addstr(timer_fila + 1, 0, linea_tiempo[: max(0, w - 1)], curses.color_pair(4))

        stdscr.refresh()

        if not tiempo_agotado:
            tecla_presionada = stdscr.getch()

            if tecla_presionada == curses.KEY_UP and posicion_seleccion > 0:
                posicion_seleccion -= 1
            elif tecla_presionada == curses.KEY_DOWN and posicion_seleccion < len(opciones) - 1:
                posicion_seleccion += 1
            elif tecla_presionada in (curses.KEY_ENTER, 10, 13):
                seleccion = posicion_seleccion
                continuar = False

        time.sleep(0.1)

    stdscr.nodelay(False)
    return seleccion, tiempo_agotado



def mostrar_feedback(stdscr, texto, opciones, seleccion, indice_correcto,
                     tiempo_agotado=False, limite_segundos=0, mensaje_extra=None, es_bonus=True):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    texto_recortado = texto[: max(0, w - 1)]
    stdscr.addstr(0, 0, texto_recortado, curses.color_pair(4))

    ultima_fila = 0

    for i, op in enumerate(opciones):
        fila = i + 2
        if fila >= h - 3:
            break

        texto_op = "  " + str(op)
        if len(texto_op) > w - 1:
            if w > 4:
                texto_op = texto_op[: w - 4] + "..."
            else:
                texto_op = texto_op[: max(0, w - 1)]

        if i == indice_correcto:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(fila, 0, texto_op)
            stdscr.attroff(curses.color_pair(2))
        elif i == seleccion:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(fila, 0, texto_op)
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(fila, 0, texto_op)

        ultima_fila = fila

    linea_mensaje = min(ultima_fila + 2, h - 2)

    if tiempo_agotado:
        mensaje = "Respuesta no registrada. ¡Se agotó el tiempo!"
    else:
        mensaje = "Presione cualquier tecla para continuar"

    mensaje_recortado = mensaje[: max(0, w - 1)]
    stdscr.addstr(linea_mensaje, 0, mensaje_recortado, curses.color_pair(4))

    if mensaje_extra and linea_mensaje + 1 < h:
        color = curses.color_pair(2) if es_bonus else curses.color_pair(3)
        extra_recortado = mensaje_extra[: max(0, w - 1)]
        stdscr.addstr(linea_mensaje + 1, 0, extra_recortado, color)

    stdscr.refresh()
    stdscr.getch()


    


def animacion_ruleta():
    elementos = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    print(f"\n{CYAN}Escogiendo pregunta al azar...{RESET}\n")
    print( " " * 30 )
    pasos_totales = 40
    sleep = 0.02
    sleep_increment = 0.004
    def reescribir_linea(contenido):
        sys.stdout.write("\x1b[1F")  
        sys.stdout.write("\r\x1b[2K" + contenido + "\n")
        sys.stdout.flush()
    for i in range(pasos_totales):
        elementos = elementos[1:] + elementos[:1]   
        tira = " ".join(elementos)

        reescribir_linea(f" {tira} ")
        winsound.Beep(300, 30)

        time.sleep(sleep)
        sleep += sleep_increment  
    winsound.Beep(600, 250)



    print(f"\n{GREEN}Pregunta seleccionada{RESET}\n")
    time.sleep(0.4)
    
def header(nombre_usuario, puntuacion, racha_actual, pregunta_actual, total_preguntas):
    return (
        f"Jugador: {nombre_usuario} | "
        f"Puntos: {puntuacion} | "
        f"Racha: {racha_actual} | "
        f"Pregunta: {pregunta_actual}/{total_preguntas}"
    )




def juego_curses(stdscr,  niveles, contrareloj , limite_segundos, nombre_usuario):
    min_altura = 28   
    min_ancho  = 80  

    while True:
        h, w = stdscr.getmaxyx()

        if h < min_altura or w < min_ancho:
            stdscr.clear()
            stdscr.addstr(0, 0, "La ventana es demasiado pequeña.", curses.A_BOLD)
            stdscr.addstr(5, 0, "Agranda la ventana y presiona cualquier tecla...")
            stdscr.refresh()
            stdscr.getch()
        else:
            break
        
    correctas = 0 
    incorrectas = 0 
    
    
    
    total_preguntas = sum(len(lista) for _, lista in niveles)
    if total_preguntas <= 0:
        total_preguntas = 1

    
    base_puntos = max(1, total_preguntas // 5)

    puntuacion = 0
    racha_actual = 0
    mejor_racha = 0
    pregunta_actual = 0
    
    for nombre_nivel, lista in niveles:
        lista = lista.copy()
        random.shuffle(lista)
        multiplicador = obtener_multiplicador_puntaje(nombre_nivel)
        
        for indice, preg in enumerate(lista):
            pregunta_actual += 1
            curses.endwin()
            animacion_ruleta()
            stdscr = curses.initscr()
            inicializar_colores()
            curses.curs_set(0)

            texto, opciones_mezcladas, indice_correcta = seleccionar_pregunta(preg)
            stdscr.clear()
            info_usuario = header(nombre_usuario,puntuacion,racha_actual,pregunta_actual, total_preguntas
)
            texto_header = f"[{nombre_nivel}] {texto}"
            stdscr.refresh()

            if contrareloj:
                seleccion, tiempo_agotado = seleccion_opcion_temporizado(
                    stdscr,
                    info_usuario,
                    texto_header,
                    opciones_mezcladas,
                    limite_segundos, 
                )
            else:
                seleccion = seleccionar_opcion(stdscr,info_usuario,texto_header, opciones_mezcladas)
                tiempo_agotado = False
                
            mensaje_extra = None
            es_bonus = True
            
            if (not tiempo_agotado) and (seleccion == indice_correcta):
                sonido_correcta()
                racha_actual += 1
                if racha_actual > mejor_racha:
                    mejor_racha = racha_actual

                puntos_pregunta = base_puntos * multiplicador

        
                bonus_racha = 0
                if racha_actual >= 3 and racha_actual < 5:
                    bonus_racha = 2         
                elif racha_actual >= 5 and racha_actual < 10:
                    bonus_racha = 5         
                elif racha_actual >= 10:
                    bonus_racha = 10        

                puntuacion += puntos_pregunta + bonus_racha
                correctas += 1
                if bonus_racha > 0:
                    sonido_bonus()

                    mensaje_extra = (
                        f"¡Racha x{racha_actual}! Bonus +{bonus_racha} puntos"
                    )
                    es_bonus = True

            else:
                sonido_incorrecta()

                if racha_actual > 1:
                    mensaje_extra = f"Racha de {racha_actual} rota..."
                    es_bonus = False
                racha_actual = 0
                incorrectas += 1


            mostrar_feedback(
                stdscr,
                texto,
                opciones_mezcladas,
                seleccion,
                indice_correcta,
                tiempo_agotado,
                limite_segundos
            )
    stdscr.clear()
    stdscr.addstr(0, 0, "Resumen de la partida", curses.color_pair(4))
    stdscr.addstr(2, 0, f"Jugador: {nombre_usuario}", curses.color_pair(6))
    stdscr.addstr(3, 0, f"Puntuación final: {puntuacion}", curses.color_pair(6))
    stdscr.addstr(4, 0, f"Preguntas respondidas: {total_preguntas}", curses.color_pair(6))
    stdscr.addstr(5, 0, f"Correctas: {correctas}", curses.color_pair(2))
    stdscr.addstr(7, 0, f"Mejor racha de aciertos: {mejor_racha}", curses.color_pair(5))
    stdscr.addstr(6, 0, f"Incorrectas: {incorrectas}", curses.color_pair(3))
    stdscr.addstr(8, 0, "Pulsa cualquier tecla para volver al menú...", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()
    
    return {"puntuacion": puntuacion, "correctas": correctas,
            "incorrectas": incorrectas, "total": total_preguntas}

def jugar(nombre_usuario):
    jugando = True
    while jugando: 
        tema= seleccionar_tema()
        niveles = seleccionar_dificultad_y_cantidad(tema)
        contra_reloj, limite_segundos = seleccionar_modo()
        
        curses.wrapper(juego_curses,niveles, contra_reloj, limite_segundos, nombre_usuario)
        menu = (
                "\n¿Qué quieres hacer ahora?\n"
                "1. Jugar otra vez con el MISMO usuario\n"
                "2. Jugar con OTRO usuario (cerrar sesión actual)\n"
                "3. Salir del juego\n"
            )
        opcion = validar_entero_menu(
                menu,
                "Elige una opción (1-3): ",
                1,
                3
            )
        if opcion == 1:
            continue
        elif opcion == 2:
            return "cambiar_usuario"
        elif opcion == 3:
            return "salir"