import pygame

class Audios:
    def __init__(self):
        pygame.mixer.init()
        self.sonido_movimiento = pygame.mixer.Sound("Resources/Audio/dragon-ball-z-heavy-punch.mp3")
        self.musica_animacion = "Resources/Audio/Dragonball Z Budokai Tenkaichi 3 OpeningIntroHD.mp3"
        self.musica_menu = "Resources/Audio/Dragon Ball Z_ Budōkai Tenkaichi 3  The Meteor (Theme of The Title ScreenMain Menu).mp3"
        self.musica_juego = "Resources/Audio/Dragon Ball Z - Música de pelea (Saga de Freezer).mp3"
        self.musica_ganador = "Resources/Audio/07-sayonara-senshi-tachi-mp3cut.mp3"

    def reproducir_sonido_movimiento(self):
        self.sonido_movimiento.play()

    def reproducir_musica_animacion(self):
        pygame.mixer.music.load(self.musica_animacion)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def reproducir_musica_menu(self):
        pygame.mixer.music.load(self.musica_menu)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def reproducir_musica_juego(self):
        pygame.mixer.music.load(self.musica_juego)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def reproducir_musica_ganador(self):
        pygame.mixer.music.load(self.musica_ganador)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)