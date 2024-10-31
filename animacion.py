import pygame
import threading

class Animacion:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.imagenes_animacion = []
        self.indice_animacion = 0
        self.imagenes_cargadas = False
        self.ancho_imagen = 0
        self.alto_imagen = 0
        self.pos_x = 0
        self.pos_y = 0

    def cargar_imagenes(self):
        self.imagenes_animacion = [pygame.image.load(f"Resources/animacion/frame-{str(i).zfill(4)}.jpg") for i in range(1, 2815)]
        self.ancho_imagen, self.alto_imagen = self.imagenes_animacion[0].get_size()
        self.pos_x = (self.ancho - self.ancho_imagen) // 2
        self.pos_y = (self.alto - self.alto_imagen) // 2
        self.imagenes_cargadas = True

    def iniciar_carga(self):
        hilo_cargar_imagenes = threading.Thread(target=self.cargar_imagenes)
        hilo_cargar_imagenes.start()

    def actualizar_animacion(self, pantalla):
        if self.imagenes_animacion:
            pantalla.fill((0, 0, 0))  # Limpiar la pantalla
            pantalla.blit(self.imagenes_animacion[self.indice_animacion], (self.pos_x, self.pos_y))
            self.indice_animacion = (self.indice_animacion + 1) % len(self.imagenes_animacion)
            pygame.display.flip()