# conexion_rasp.py
import socket
import threading
import pygame

cliente_socket = None

# Función para conectar con la Raspberry Pi Pico W
def conectar(host, port):
    global cliente_socket
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        print(f"Conectado a {host}:{port}")
    except Exception as e:
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
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
    elif comando == 'R':
        print("Navegación derecha")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
    elif comando == 'U':
        print("Navegación arriba")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w))
    elif comando == 'D':
        print("Navegación abajo")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s))
    elif comando == 'E':
        print("Botón Enter")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
    elif comando == 'S':
        print("Accionar solenoide")
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))

# Hilo para recibir datos
def iniciar_hilo_recepcion():
    hilo_recibir = threading.Thread(target=recibir_datos)
    hilo_recibir.daemon = True
    hilo_recibir.start()