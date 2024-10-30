# Raspberry Pi Pico W - MicroPython
import time
import network
import socket
from machine import Pin, ADC

# Configuración de pines
led1 = Pin(2, Pin.OUT)
led2 = Pin(3, Pin.OUT)
boton_cambio_jugador = Pin(7, Pin.IN, Pin.PULL_DOWN)
zonas_anotacion = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN), Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(14, Pin.IN, Pin.PULL_DOWN), Pin(15, Pin.IN, Pin.PULL_DOWN)]
registro_corrimiento = [Pin(24, Pin.OUT), Pin(25, Pin.OUT)]
leds_cambio_jugador = [Pin(29, Pin.OUT), Pin(32, Pin.OUT)]
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

def iniciar_conexion():
    global conn, addr
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print(f"Conectado con {addr}")

iniciar_conexion()

# Función para enviar datos a la laptop
def enviar_datos(codigo):
    try:
        conn.send(codigo.encode())
    except OSError as e:
        print(f"Error al enviar datos: {e}")
        iniciar_conexion()

# Función para leer el valor del potenciómetro
def leer_potenciometro():
    valor = potenciometro.read_u16() >> 12  # Escala de 0-15
    return valor

# Función para parpadear LEDs
def parpadear_leds(leds, duracion=3, intervalo=0.3):
    end_time = time.time() + duracion
    while time.time() < end_time:
        for led in leds:
            led.toggle()
        time.sleep(intervalo)
    for led in leds:
        led.value(0)  # Asegurarse de que los LEDs estén apagados al final

# Función para manejar anotaciones
def manejar_anotacion(zona):
    puntos = 0
    if zona == 10:
        puntos = 10
    elif zona == 11:
        puntos = 20
    elif zona == 12:
        puntos = 30
    elif zona == 14:
        puntos = 40
    elif zona == 15:
        puntos = 50
    print(f"Anotación en zona {zona} con {puntos} puntos")
    enviar_datos(f"Z{zona}")  # Enviar datos de la zona anotada
    parpadear_leds(leds_cambio_jugador)  # Parpadear LEDs de cambio de jugador

# Bucle principal
while True:
    try:
        # Leer potenciómetro para selección del jugador
        jugador_seleccionado = leer_potenciometro()
        print(f"Jugador seleccionado: {jugador_seleccionado}")

        # Detectar cambio de jugador
        if boton_cambio_jugador.value() == 1:
            print("Cambio de jugador detectado")
            enviar_datos('A')  # Código para cambio de jugador
            time.sleep(0.5)

        # Detectar anotaciones
        for i, zona in enumerate(zonas_anotacion):
            if zona.value() == 1:
                manejar_anotacion(10 + i)
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
    except OSError as e:
        print(f"Error en la conexión: {e}")
        iniciar_conexion()

# Cerrar la conexión
conn.close()