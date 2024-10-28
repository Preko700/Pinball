# Raspberry Pi Pico W - MicroPython
import time
import network
import socket
from machine import Pin, ADC

# Configuración de pines
led1 = Pin(2, Pin.OUT)
led2 = Pin(3, Pin.OUT)
boton_cambio_jugador = Pin(4, Pin.IN, Pin.PULL_DOWN)
boton_navegacion_izquierda = Pin(5, Pin.IN, Pin.PULL_DOWN)
boton_navegacion_derecha = Pin(6, Pin.IN, Pin.PULL_DOWN)
boton_enter = Pin(7, Pin.IN, Pin.PULL_DOWN)
boton_solenoide = Pin(8, Pin.IN, Pin.PULL_DOWN)
potenciometro = ADC(0)

# Conexión WiFi
ssid = 'PutiHouse'
password = 'N-A-C-E-J '
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Conectando al WiFi...")
    time.sleep(1)

print("Conectado al WiFi")
ip = wlan.ifconfig()[0]

# Configuración de socket
host = '192.168.100.30'  
port = 8266

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

print("Esperando conexión del cliente...")
conn, addr = s.accept()
print(f"Conectado con {addr}")

# Función para enviar datos a la laptop
def enviar_datos(codigo):
    conn.send(codigo.encode())

# Función para leer el valor del potenciómetro
def leer_potenciometro():
    valor = potenciometro.read_u16() >> 12  # Escala de 0-15
    return valor

# Bucle principal
while True:
    # Leer potenciómetro para selección del jugador
    jugador_seleccionado = leer_potenciometro()
    print(f"Jugador seleccionado: {jugador_seleccionado}")

    # Detectar cambio de jugador
    if boton_cambio_jugador.value() == 1:
        print("Cambio de jugador detectado")
        enviar_datos('A')  # Código para cambio de jugador
        time.sleep(0.5)

    # Detectar navegación izquierda
    if boton_navegacion_izquierda.value() == 1:
        print("Navegación izquierda detectada")
        enviar_datos('L')  # Código para navegación izquierda
        time.sleep(0.5)

    # Detectar navegación derecha
    if boton_navegacion_derecha.value() == 1:
        print("Navegación derecha detectada")
        enviar_datos('R')  # Código para navegación derecha
        time.sleep(0.5)

    # Detectar botón Enter
    if boton_enter.value() == 1:
        print("Botón Enter detectado")
        enviar_datos('E')  # Código para Enter
        time.sleep(0.5)

    # Detectar botón Solenoide
    if boton_solenoide.value() == 1:
        print("Botón Solenoide detectado")
        enviar_datos('S')  # Código para Solenoide
        time.sleep(0.5)

    # Encender LED para indicación
    led1.toggle()
    time.sleep(1)
    led2.toggle()
    time.sleep(1)

    # Recibir datos desde la laptop
    datos = conn.recv(1024).decode()
    if datos:
        print(f"Datos recibidos: {datos}")
        # Manejar los códigos de la A a la M
        if datos == 'B':
            led1.value(1)
            time.sleep(3)
            led1.value(0)

# Cerrar la conexión
conn.close()    