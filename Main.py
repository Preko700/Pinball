# Laptop - Python con Pygame
import pygame
import random
import socket
import threading

# Configuración inicial
pygame.init()
ancho, alto = 1280, 720
pantalla = pygame.display.set_mode((ancho, alto)) 
pygame.display.set_caption("Juego de Pinball Interactivo")
reloj = pygame.time.Clock()

# Conexión con la Raspberry Pi Pico W
host = '192.168.100.30'
port = 8266

try:
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, port))
except socket.error as e:
    print(f"Error al conectar con {host}:{port} - {e}")
    cliente_socket = None

# Función para enviar datos a la Pico W
def enviar_datos(codigo):
    if cliente_socket:
        cliente_socket.send(codigo.encode())

# Función para recibir datos de la Pico W
def recibir_datos():
    while True:
        datos = cliente_socket.recv(1024).decode()
        if datos:
            print(f"Datos recibidos: {datos}")
            manejar_comandos(datos)

# Función para manejar los comandos recibidos
def manejar_comandos(comando):
    if comando == 'L':
        print("Navegación izquierda")
        # Implementar lógica de navegación izquierda
    elif comando == 'R':
        print("Navegación derecha")
        # Implementar lógica de navegación derecha
    elif comando == 'E':
        print("Botón Enter")
        # Implementar lógica de botón Enter
    elif comando == 'S':
        print("Accionar solenoide")
        # Implementar lógica para accionar el solenoide

# Hilo para recibir datos
hilo_recibir = threading.Thread(target=recibir_datos)
hilo_recibir.daemon = True
hilo_recibir.start()

# Lista para almacenar las imágenes de la animación
imagenes_animacion = []
indice_animacion = 0
imagenes_cargadas = False

# Función para cargar imágenes de la animación
def cargar_imagenes():
    global imagenes_animacion, imagenes_cargadas
    imagenes_animacion = [pygame.image.load(f"Resources/animacion/frame-{str(i).zfill(4)}.jpg") for i in range(1, 2815)]
    # Obtener el tamaño de la primera imagen para centrar todas las imágenes
    global ancho_imagen, alto_imagen, pos_x, pos_y
    ancho_imagen, alto_imagen = imagenes_animacion[0].get_size()
    pos_x = (ancho - ancho_imagen) // 2
    pos_y = (alto - alto_imagen) // 2
    imagenes_cargadas = True

# Hilo para cargar imágenes
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

# Bucle principal del juego
pantalla_carga() 
pygame.time.wait(20000)  # Esperar 20000 milisegundos (5 segundos)
# Sonido y música
pygame.mixer.music.load("Resources/Audio/Dragonball Z Budokai Tenkaichi 3 OpeningIntroHD.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    if imagenes_cargadas:
        actualizar_animacion()
    else:
        pantalla_carga()

    reloj.tick(26)  # Controlar la velocidad de la animación

pygame.quit()
