# main.py
import pygame
import threading
from conexion_rasp import conectar, enviar_datos, iniciar_hilo_recepcion

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

# Lista para almacenar las imágenes de la animación
imagenes_animacion = []
indice_animacion = 0
imagenes_cargadas = False

# Cargar fondo del menú principal
fondo_menu = pygame.image.load("Resources/Images/wallpaper.jpg")

# Cargar fondo del juego
fondo_juego = pygame.image.load("Resources/Images/versus.jpg")

# Cargar imágenes de los íconos de los jugadores
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

# Lista de nombres de los íconos
nombres_iconos = list(iconos_jugadores.keys())

# Función para cargar imágenes de la animación
def cargar_imagenes():
    global imagenes_animacion, imagenes_cargadas
    imagenes_animacion = [pygame.image.load(f"Resources/animacion/frame-{str(i).zfill(4)}.jpg") for i in range(1, 2815)]
    global ancho_imagen, alto_imagen, pos_x, pos_y
    ancho_imagen, alto_imagen = imagenes_animacion[0].get_size()
    pos_x = (ancho - ancho_imagen) // 2
    pos_y = (alto - alto_imagen) // 2
    imagenes_cargadas = True

hilo_cargar_imagenes = threading.Thread(target=cargar_imagenes)
hilo_cargar_imagenes.start()

# Función para actualizar y dibujar la animación
def actualizar_animacion():
    global indice_animacion
    if imagenes_animacion:
        pantalla.fill((0, 0, 0))  # Limpiar la pantalla
        pantalla.blit(imagenes_animacion[indice_animacion], (pos_x, pos_y))
        indice_animacion = (indice_animacion + 1) % len(imagenes_animacion)
        pygame.display.flip()

# Función para mostrar la pantalla de carga
def pantalla_carga():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Cargando...", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2))
    pygame.display.flip()

# Pantalla de presentación
def pantalla_presentacion():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Juego de Pinball Interactivo", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 - 100))
    texto = fuente.render("Presione Enter para comenzar", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 + 100))
    pygame.display.flip()

# Pantalla de configuración inicial
def pantalla_configuracion():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Configuración Inicial", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 - 100))

    opciones = ["1 Jugador", "2 Jugadores"]
    for i, opcion in enumerate(opciones):
        color = (255, 255, 0) if i == opcion_seleccionada else (100, 100, 100)
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 + i * 100))

    pygame.display.flip()

# Pantalla de información complementaria
def pantalla_informacion():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Acerca de los Autores", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, 50))

    # Cargar imágenes de los autores
    foto_adrian = pygame.image.load("Resources/Images/adrian.jpg")
    foto_ariel = pygame.image.load("Resources/Images/ariel.jpg")

    # Redimensionar imágenes
    foto_adrian = pygame.transform.scale(foto_adrian, (150, 150))
    foto_ariel = pygame.transform.scale(foto_ariel, (150, 150))

    # Mostrar imágenes
    pantalla.blit(foto_adrian, (ancho // 4 - 75, 150))
    pantalla.blit(foto_ariel, (3 * ancho // 4 - 75, 150))

    # Mostrar información de los autores
    info = [
        "Nombres: Adrián Monge Mairena y Ariel Gómez Alvarado",
        "Identificación: 2023800088",
        "Asignatura: Fundamentos de sistemas computacionales (CE1104)",
        "Carrera: Ingeniería en Computadores",
        "Año: 2024",
        "Profesor: Milton Enrique Villegas Lemus",
        "País de Producción: Costa Rica",
        "Versión del programa: 1.6",
        "Información de ayuda: Para el buen uso del programa, siga las instrucciones en pantalla y asegúrese de que todos los componentes estén correctamente conectados."
    ]

    y_offset = 350
    for line in info:
        texto = fuente.render(line, True, (255, 255, 255))
        pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, y_offset))
        y_offset += 50

    pygame.display.flip()

# Pantalla del menú principal
def pantalla_menu_principal(opcion_seleccionada):
    pantalla.blit(fondo_menu, (0, 0))  # Mostrar fondo del menú principal
    fuente = pygame.font.Font(None, 74)
    opciones = ["Jugar", "About"]
    for i, opcion in enumerate(opciones):
        color = (255, 255, 0) if i == opcion_seleccionada else (100, 100, 100)
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (50, alto - 150 + i * 100))  # Colocar en la parte inferior izquierda
    pygame.display.flip()

# Pantalla de selección de ícono
def pantalla_seleccion_icono(jugador, opcion_icono_seleccionada):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render(f"Seleccione un ícono para el jugador {jugador}", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, 50))

    # Títulos "Heroes" y "Villanos"
    fuente_heroes = pygame.font.Font(None, 50)
    texto_heroes = fuente_heroes.render("Heroes", True, (0, 0, 255))
    pantalla.blit(texto_heroes, (ancho // 4 - texto_heroes.get_width() // 2, 150))

    fuente_villanos = pygame.font.Font(None, 50)
    texto_villanos = fuente_villanos.render("Villanos", True, (255, 0, 0))
    pantalla.blit(texto_villanos, (3 * ancho // 4 - texto_villanos.get_width() // 2, 150))

    iconos = list(iconos_jugadores.values())
    nombres_iconos = list(iconos_jugadores.keys())
    for i, icono in enumerate(iconos):
        pantalla.blit(icono, (50 + i * 200, alto // 2 - 75))
        nombre_icono = fuente.render(nombres_iconos[i], True, (255, 255, 255))
        pantalla.blit(nombre_icono, (50 + i * 200, alto // 2 + 100))

    # Dibujar recuadro amarillo alrededor del ícono seleccionado
    pygame.draw.rect(pantalla, (255, 255, 0), (50 + opcion_icono_seleccionada * 200 - 10, alto // 2 - 85, 170, 220), 5)

    pygame.display.flip()

# Pantalla del juego
def pantalla_juego():
    pantalla.fill((0, 0, 0))  # Limpiar la pantalla
    pantalla.blit(fondo_juego, (0, 0))  # Mostrar fondo del juego centrado
    fuente = pygame.font.Font(None, 100)  # Fuente más grande para los datos de los jugadores

    # Mostrar información del jugador 1
    if icono_jugador1:
        pantalla.blit(icono_jugador1, (ancho // 4 - 75, alto // 2 - 150))
        texto_nombre = fuente.render(f"{nombres_iconos[list(iconos_jugadores.values()).index(icono_jugador1)]}", True, (255, 255, 255))
        pantalla.blit(texto_nombre, (ancho // 4 - texto_nombre.get_width() // 2, alto // 2 + 50))
        texto_puntaje = fuente.render(f"Puntaje: {puntaje_jugador1}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (ancho // 4 - texto_puntaje.get_width() // 2, alto // 2 + 150))

    # Mostrar información del jugador 2
    if jugadores == 2 and icono_jugador2:
        pantalla.blit(icono_jugador2, (3 * ancho // 4 - 75, alto // 2 - 150))
        texto_nombre = fuente.render(f"{nombres_iconos[list(iconos_jugadores.values()).index(icono_jugador2)]}", True, (255, 255, 255))
        pantalla.blit(texto_nombre, (3 * ancho // 4 - texto_nombre.get_width() // 2, alto // 2 + 50))
        texto_puntaje = fuente.render(f"Puntaje: {puntaje_jugador2}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (3 * ancho // 4 - texto_puntaje.get_width() // 2, alto // 2 + 150))

    pygame.display.flip()

# Bucle principal del juego
pantalla_carga()
pygame.time.wait(20000)  # Esperar 20000 milisegundos (20 segundos)
# Sonido y música
pygame.mixer.music.load("Resources/Audio/Dragonball Z Budokai Tenkaichi 3 OpeningIntroHD.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Cargar sonido de movimiento
sonido_movimiento = pygame.mixer.Sound("Resources/Audio/dragon-ball-z-heavy-punch.mp3")

ejecutando = True
estado = "animacion"
opcion_seleccionada = 0
opcion_icono_seleccionada = 0
jugadores = 1
icono_jugador1 = None
icono_jugador2 = None
puntaje_jugador1 = 0
puntaje_jugador2 = 0
jugador_actual = 1

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                sonido_movimiento.play()  # Reproducir sonido de movimiento
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
                        pygame.mixer.music.load("Resources/Audio/Dragon Ball Z - Música de pelea (Saga de Freezer).mp3")
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                elif estado == "seleccion_icono2":
                    icono_jugador2 = list(iconos_jugadores.values())[opcion_icono_seleccionada]
                    estado = "juego"
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Resources/Audio/Dragon Ball Z - Música de pelea (Saga de Freezer).mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
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
                pygame.mixer.music.load("Resources/Audio/Dragon Ball Z_ Budōkai Tenkaichi 3  The Meteor (Theme of The Title ScreenMain Menu).mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)

    if estado == "animacion":
        if imagenes_cargadas:
            actualizar_animacion()
        else:
            pantalla_carga()
    elif estado == "menu_principal":
        pantalla_menu_principal(opcion_seleccionada)
    elif estado == "configuracion":
        pantalla_configuracion()
    elif estado == "informacion":
        pantalla_informacion()
    elif estado == "seleccion_icono1":
        pantalla_seleccion_icono(1, opcion_icono_seleccionada)
    elif estado == "seleccion_icono2":
        pantalla_seleccion_icono(2, opcion_icono_seleccionada)
    elif estado == "juego":
        pantalla_juego()

    reloj.tick(26)  # Controlar la velocidad de la animación

pygame.quit()