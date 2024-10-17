import pygame
import random
import serial
import time

# Inicializar Pygame
pygame.init()

# Configuración de la ventana de juego
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pinball Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración del puerto serie para la Raspberry Pi
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

# Función para leer el valor del potenciómetro
def read_potentiometer():
    ser.write(b'R')
    value = ser.readline().decode('utf-8').strip()
    return int(value) if value else 0

# Función para controlar los LEDs
def control_leds(score):
    if score > 100:
        ser.write(b'L1')
    else:
        ser.write(b'L0')

# Clase para la bola
class Ball:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.radius = 10
        self.dx = random.choice([-5, 5])
        self.dy = random.choice([-5, 5])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Colisiones con los bordes
        if self.x <= 0 or self.x >= 800:
            self.dx = -self.dx
        if self.y <= 0 or self.y >= 600:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

# Clase para el juego
class PinballGame:
    def __init__(self):
        self.ball = Ball()
        self.score = 0
        self.running = True

    def update(self):
        self.ball.move()
        self.score += 1
        control_leds(self.score)

    def draw(self):
        screen.fill(BLACK)
        self.ball.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            pygame.time.delay(30)

# Pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render('Pinball Game', True, WHITE)
    screen.blit(text, (200, 250))
    pygame.display.flip()
    time.sleep(2)

# Pantalla de resultados
def show_end_screen(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(text, (200, 250))
    pygame.display.flip()
    time.sleep(2)

# Función principal
def main():
    show_start_screen()
    game = PinballGame()
    game.run()
    show_end_screen(game.score)
    pygame.quit()

if __name__ == '__main__':
    main()