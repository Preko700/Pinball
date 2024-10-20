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

# Sonido y música
pygame.mixer.music.load("Resources/Audio/Dragonball Z Budokai Tenkaichi 3 OpeningIntroHD.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Pinball Interactivo", True, (255, 255, 255))
    pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 3))
    pygame.display.flip()

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

# Hilo para recibir datos
hilo_recibir = threading.Thread(target=recibir_datos)
hilo_recibir.daemon = True
hilo_recibir.start()

# Cargar imágenes de la animación
imagenes_animacion = [pygame.image.load(f"animacion/frame_{i}.png") for i in range(1, 11)]
indice_animacion = 0
pos_x, pos_y = ancho // 2, alto // 2

# Función para actualizar y dibujar la animación
def actualizar_animacion():
    global indice_animacion
    pantalla.fill((0, 0, 0))  # Limpiar la pantalla
    pantalla.blit(imagenes_animacion[indice_animacion], (pos_x, pos_y))
    indice_animacion = (indice_animacion + 1) % len(imagenes_animacion)
    pygame.display.flip()

# Bucle principal del juego
pantalla_inicio()
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    actualizar_animacion()
    reloj.tick(10)  # Controlar la velocidad de la animación

pygame.quit()
