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
    pygame.display.flip()

# Pantalla de información complementaria
def pantalla_informacion():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Acerca del Autor", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 - 100))
    pygame.display.flip()

# Pantalla del menú principal
def pantalla_menu_principal(opcion_seleccionada):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    opciones = ["Jugar", "About"]
    for i, opcion in enumerate(opciones):
        color = (255, 255, 255) if i == opcion_seleccionada else (100, 100, 100)
        texto = fuente.render(opcion, True, color)
        pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 2 - 100 + i * 100))
    pygame.display.flip()

# Bucle principal del juego
pantalla_carga()
pygame.time.wait(20000)  # Esperar 20000 milisegundos (20 segundos)
# Sonido y música
pygame.mixer.music.load("Resources/Audio/Dragonball Z Budokai Tenkaichi 3 OpeningIntroHD.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

ejecutando = True
estado = "animacion"
opcion_seleccionada = 0

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                if estado == "presentacion":
                    estado = "configuracion"
                elif estado == "configuracion":
                    estado = "juego"
                elif estado == "informacion":
                    estado = "presentacion"
                elif estado == "menu_principal":
                    if opcion_seleccionada == 0:
                        estado = "configuracion"
                    elif opcion_seleccionada == 1:
                        estado = "informacion"
            elif evento.key == pygame.K_i:
                estado = "informacion"
            elif evento.key == pygame.K_w:
                opcion_seleccionada = (opcion_seleccionada - 1) % 2
            elif evento.key == pygame.K_s:
                opcion_seleccionada = (opcion_seleccionada + 1) % 2
            elif evento.key == pygame.K_a:
                # Implementar lógica para navegación izquierda
                pass
            elif evento.key == pygame.K_d:
                # Implementar lógica para navegación derecha
                pass
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
    elif estado == "juego":
        if imagenes_cargadas:
            actualizar_animacion()
        else:
            pantalla_carga()

    reloj.tick(26)  # Controlar la velocidad de la animación

pygame.quit()
