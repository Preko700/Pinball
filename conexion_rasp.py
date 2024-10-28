# conexion_rasp.py
import socket
import threading

cliente_socket = None

# Función para conectar con la Raspberry Pi Pico W
def conectar(host, port):
    global cliente_socket
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        print(f"Conectado a {host}:{port}")
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
def iniciar_hilo_recepcion():
    hilo_recibir = threading.Thread(target=recibir_datos)
    hilo_recibir.daemon = True
    hilo_recibir.start()