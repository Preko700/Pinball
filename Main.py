import pygame
import random
import socket
import threading
from circuito_menos_3 import CircuitoMenos3
from pantallas import Pantallas
from audios import Audios
from animacion import Animacion
from conexion_rasp import conectar, enviar_datos

# Configuración inicial
pygame.init()
ancho, alto = 1280, 720
pantalla = pygame.display.set_mode((ancho, alto)) 
pygame.display.set_caption("Juego de Pinball Interactivo")
reloj = pygame.time.Clock()

# Inicialización de clases
pantallas = Pantallas(ancho, alto)
audios = Audios()
animacion = Animacion(ancho, alto)
circuito_menos_3 = CircuitoMenos3()

# Conexión con la Raspberry Pi Pico W
host = '192.168.100.30'
port = 8266
modo_pruebas = False

try:
    conectar(host, port)
except Exception as e:
    print(f"No se pudo conectar con la Raspberry Pi Pico W: {e}")
    print("Iniciando en modo de pruebas...")
    modo_pruebas = True

# Variables del juego
estado = "animacion"
opcion_seleccionada = 0
opcion_icono_seleccionada = 0
jugador_actual = 1
puntaje_jugador1 = 0
puntaje_jugador2 = 0
tiros_jugador1 = 0
tiros_jugador2 = 0
jugadores = 2  # Número de jugadores
iconos_jugadores = {"Jugador1": "icono1.png", "Jugador2": "icono2.png"}  # Ejemplo de iconos

def reiniciar_variables():
    global estado, opcion_seleccionada, opcion_icono_seleccionada, jugador_actual
    global puntaje_jugador1, puntaje_jugador2, tiros_jugador1, tiros_jugador2, jugadores
    estado = "animacion"
    opcion_seleccionada = 0
    opcion_icono_seleccionada = 0
    jugador_actual = 1
    puntaje_jugador1 = 0
    puntaje_jugador2 = 0
    tiros_jugador1 = 0
    tiros_jugador2 = 0
    jugadores = 2

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                if estado in ["seleccion_icono1", "seleccion_icono2"]:
                    opcion_icono_seleccionada = (opcion_icono_seleccionada - 1) % len(iconos_jugadores)
            elif evento.key == pygame.K_d:
                if estado in ["seleccion_icono1", "seleccion_icono2"]:
                    opcion_icono_seleccionada = (opcion_icono_seleccionada + 1) % len(iconos_jugadores)
            elif evento.key == pygame.K_SPACE and estado == "animacion":
                estado = "menu_principal"
                pygame.mixer.music.stop()
                audios.reproducir_musica_menu()
            elif evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5] and estado == "juego":
                puntos = int(evento.unicode) * 100
                if jugador_actual == 1:
                    puntaje_jugador1 += puntos
                    tiros_jugador1 += 1
                    if tiros_jugador1 >= 3:
                        if jugadores == 1:
                            estado = "ganador"
                            pygame.mixer.music.stop()
                            audios.reproducir_musica_ganador()
                        else:
                            jugador_actual = 2
                elif jugador_actual == 2:
                    puntaje_jugador2 += puntos
                    tiros_jugador2 += 1
                    if tiros_jugador2 >= 3:
                        if puntaje_jugador1 == puntaje_jugador2:
                            estado = "empate"
                        else:
                            estado = "ganador"
                        pygame.mixer.music.stop()
                        audios.reproducir_musica_ganador()
            elif evento.key == pygame.K_i:
                estado = "informacion"
            elif evento.key == pygame.K_w:
                if estado in ["menu_principal", "configuracion"]:
                    opcion_seleccionada = (opcion_seleccionada - 1) % 2
            elif evento.key == pygame.K_s:
                if estado in ["menu_principal", "configuracion"]:
                    opcion_seleccionada = (opcion_seleccionada + 1) % 2

    if estado == "animacion":
        if animacion.imagenes_cargadas:
            animacion.actualizar_animacion(pantalla)
        else:
            pantallas.pantalla_carga(pantalla)
    elif estado == "menu_principal":
        pantallas.pantalla_menu_principal(pantalla, opcion_seleccionada)
    elif estado == "configuracion":
        pantallas.pantalla_configuracion(pantalla, opcion_seleccionada)
    elif estado == "informacion":
        pantallas.pantalla_informacion(pantalla)
    elif estado == "seleccion_icono1":
        pantallas.pantalla_seleccion_icono(pantalla, 1, opcion_icono_seleccionada, iconos_jugadores)
    elif estado == "seleccion_icono2":
        pantallas.pantalla_seleccion_icono(pantalla, 2, opcion_icono_seleccionada, iconos_jugadores)
    elif estado == "juego":
        pantallas.pantalla_juego(pantalla, iconos_jugadores["Jugador1"], iconos_jugadores["Jugador2"], list(iconos_jugadores.keys()), puntaje_jugador1, puntaje_jugador2, jugadores, jugador_actual, iconos_jugadores)
    elif estado == "ganador":
        if puntaje_jugador1 > puntaje_jugador2:
            ganador_icono = iconos_jugadores["Jugador1"]
            ganador_nombre = "Jugador1"
            ganador_puntaje = puntaje_jugador1
        else:
            ganador_icono = iconos_jugadores["Jugador2"]
            ganador_nombre = "Jugador2"
            ganador_puntaje = puntaje_jugador2
        # Procesar el puntaje del ganador con el circuito menos 3
        circuito_menos_3.habilitar()
        resultado_bits = circuito_menos_3.procesar_puntaje(ganador_puntaje)
        print(f"Resultado después de restar 3: {resultado_bits}")
        circuito_menos_3.deshabilitar()
        if not modo_pruebas:
            enviar_datos(f"B{resultado_bits}")  # Enviar los bits resultantes a la Raspberry Pi Pico W
        pantallas.pantalla_ganador(pantalla, ganador_icono, ganador_nombre, ganador_puntaje)
    elif estado == "empate":
        pantallas.pantalla_empate(pantalla, iconos_jugadores["Jugador1"], iconos_jugadores["Jugador2"], "Jugador1", "Jugador2")

    reloj.tick(26)  # Controlar la velocidad de la animación

pygame.quit()