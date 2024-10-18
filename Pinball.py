import pygame
import time

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pinball Game")

# Pantalla de inicio
def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render('Pinball Game', True, WHITE)
    screen.blit(text, (200, 250))
    pygame.display.flip()
    time.sleep(2)

# Pantalla de configuración
def show_config_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render('Configuración', True, WHITE)
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
    show_config_screen()
    game = PinballGame()
    game.run()
    show_end_screen(game.score)
    pygame.quit()

if __name__ == '__main__':
    main()