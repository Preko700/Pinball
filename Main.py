# main.py
import pygame
from conexion_rasp import conectar, enviar_datos, iniciar_hilo_recepcion
from pantallas import Pantallas
from animacion import Animacion
from audios import Audios

# Configuración inicial
pygame.init()
ancho, alto = 1280, 720
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego de Pinball Interactivo")
reloj = pygame.time.Clock()

# Conexión con la Raspberry Pi Pico W
host = '192.168.100.30'
port = 8266

conectar(host, port)
iniciar_hilo_recepcion()

# Instanciar clases
pantallas = Pantallas(ancho, alto)
animacion = Animacion(ancho, alto)
audios = Audios()

# Lista para almacenar las imágenes de la animación
animacion.iniciar_carga()

# Definir iconos_jugadores
iconos_jugadores = {
    "goku": pygame.image.load("Resources/Images/goku.jpg"),
    "gotenks": pygame.image.load("Resources/Images/gotenks.jpg"),
    "vegeta": pygame.image.load("Resources/Images/vegeta.jpg"),
    "majin": pygame.image.load("Resources/Images/majin.jpg"),
    "broly": pygame.image.load("Resources/Images/broly.jpg"),
    "janemba": pygame.image.load("Resources/Images/janemba.jpg")
}

# Redimensionar imágenes de los íconos
for key in iconos_jugadores:
    iconos_jugadores[key] = pygame.transform.scale(iconos_jugadores[key], (150, 150))

# Variables del juego
opcion_seleccionada = 0
opcion_icono_seleccionada = 0
jugadores = 1
icono_jugador1 = None
icono_jugador2 = None
puntaje_jugador1 = 0
puntaje_jugador2 = 0
jugador_actual = 1

# Bucle principal del juego
pantallas.pantalla_carga(pantalla)
pygame.time.wait(20000)  # Esperar 20000 milisegundos (20 segundos)
audios.reproducir_musica_animacion()

ejecutando = True
estado = "animacion"

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                audios.reproducir_sonido_movimiento()
                if estado == "presentacion":
                    estado = "configuracion"
                elif estado == "configuracion":
                    if opcion_seleccionada == 0:
                        jugadores = 1
                    elif opcion_seleccionada == 1:
                        jugadores = 2
                    enviar_datos(f"J{jugadores}")  # Informar a la Raspberry Pi Pico W sobre el número de jugadores
                    estado = "seleccion_icono1"
                elif estado == "seleccion_icono1":
                    icono_jugador1 = list(iconos_jugadores.values())[opcion_icono_seleccionada]
                    if jugadores == 2:
                        estado = "seleccion_icono2"
                    else:
                        estado = "juego"
                        pygame.mixer.music.stop()
                        audios.reproducir_musica_juego()
                elif estado == "seleccion_icono2":
                    icono_jugador2 = list(iconos_jugadores.values())[opcion_icono_seleccionada]
                    estado = "juego"
                    pygame.mixer.music.stop()
                    audios.reproducir_musica_juego()
                elif estado == "informacion":
                    estado = "menu_principal"  # Volver al menú principal desde "About"
                elif estado == "menu_principal":
                    if opcion_seleccionada == 0:
                        estado = "configuracion"
                    elif opcion_seleccionada == 1:
                        estado = "informacion"
            elif evento.key == pygame.K_i:
                estado = "informacion"
            elif evento.key == pygame.K_w:
                if estado in ["menu_principal", "configuracion"]:
                    opcion_seleccionada = (opcion_seleccionada - 1) % 2
            elif evento.key == pygame.K_s:
                if estado in ["menu_principal", "configuracion"]:
                    opcion_seleccionada = (opcion_seleccionada + 1) % 2
            elif evento.key == pygame.K_a:
                if estado in ["seleccion_icono1", "seleccion_icono2"]:
                    opcion_icono_seleccionada = (opcion_icono_seleccionada - 1) % len(iconos_jugadores)
            elif evento.key == pygame.K_d:
                if estado in ["seleccion_icono1", "seleccion_icono2"]:
                    opcion_icono_seleccionada = (opcion_icono_seleccionada + 1) % len(iconos_jugadores)
            elif evento.key == pygame.K_SPACE and estado == "animacion":
                estado = "menu_principal"
                pygame.mixer.music.stop()
                audios.reproducir_musica_menu()

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
        pantallas.pantalla_juego(pantalla, icono_jugador1, icono_jugador2, list(iconos_jugadores.keys()), puntaje_jugador1, puntaje_jugador2, jugadores, iconos_jugadores)

    reloj.tick(26)  # Controlar la velocidad de la animación

pygame.quit()