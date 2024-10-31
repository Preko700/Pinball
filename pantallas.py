import pygame

class Pantallas:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.fondo_menu = pygame.image.load("Resources/Images/fondo_menu.jpg")
        self.fondo_juego = pygame.image.load("Resources/Images/versus.jpg")

    def pantalla_carga(self, pantalla):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("Cargando...", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, self.alto // 2))
        pygame.display.flip()

    def pantalla_presentacion(self, pantalla):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("Juego de Pinball Interactivo", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, self.alto // 2 - 100))
        texto = fuente.render("Presione Enter para comenzar", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, self.alto // 2 + 100))
        pygame.display.flip()

    def pantalla_configuracion(self, pantalla, opcion_seleccionada):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("Configuración Inicial", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, self.alto // 2 - 100))

        opciones = ["1 Jugador", "2 Jugadores"]
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == opcion_seleccionada else (100, 100, 100)
            texto = fuente.render(opcion, True, color)
            pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, self.alto // 2 + i * 100))

        pygame.display.flip()

    def pantalla_informacion(self, pantalla):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 50)
        texto = fuente.render("Acerca de los Autores", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, 50))

        # Cargar imágenes de los autores
        foto_adrian = pygame.image.load("Resources/Images/adrian.jpg")
        foto_ariel = pygame.image.load("Resources/Images/ariel.jpg")

        # Redimensionar imágenes
        foto_adrian = pygame.transform.scale(foto_adrian, (150, 150))
        foto_ariel = pygame.transform.scale(foto_ariel, (150, 150))

        # Mostrar imágenes
        pantalla.blit(foto_adrian, (self.ancho // 4 - 75, 150))
        pantalla.blit(foto_ariel, (3 * self.ancho // 4 - 75, 150))

        # Mostrar información de los autores
        info = [
            "Nombres: Adrián Monge Mairena y Ariel Gómez Alvarado",
            "Identificación: 2023800088",
            "Asignatura: Fundamentos de sistemas computacionales (CE1104)",
            "Carrera: Ingeniería en Computadores",
            "Año: 2024",
            "Profesor: Milton Enrique Villegas Lemus",
            "País de Producción: Costa Rica",
            "Versión del programa: 1.6",
            "Información de ayuda: Para el buen uso del programa, siga las instrucciones en pantalla y asegúrese de que todos los componentes estén correctamente conectados."
        ]

        y_offset = 350
        for line in info:
            texto = fuente.render(line, True, (255, 255, 255))
            pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, y_offset))
            y_offset += 50

        pygame.display.flip()

    def pantalla_menu_principal(self, pantalla, opcion_seleccionada):
        pantalla.blit(self.fondo_menu, (0, 0))  # Mostrar fondo del menú principal
        fuente = pygame.font.Font(None, 74)
        opciones = ["Jugar", "About"]
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == opcion_seleccionada else (100, 100, 100)
            texto = fuente.render(opcion, True, color)
            pantalla.blit(texto, (50, self.alto - 150 + i * 100))  # Colocar en la parte inferior izquierda
        pygame.display.flip()

    def pantalla_seleccion_icono(self, pantalla, jugador, opcion_icono_seleccionada, iconos_jugadores):
        pantalla.fill((0, 0, 0))
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render(f"Seleccione un ícono para el jugador {jugador}", True, (255, 255, 255))
        pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, 50))

        # Títulos "Heroes" y "Villanos"
        fuente_heroes = pygame.font.Font(None, 50)
        texto_heroes = fuente_heroes.render("Heroes", True, (0, 0, 255))
        pantalla.blit(texto_heroes, (self.ancho // 4 - texto_heroes.get_width() // 2, 150))

        fuente_villanos = pygame.font.Font(None, 50)
        texto_villanos = fuente_villanos.render("Villanos", True, (255, 0, 0))
        pantalla.blit(texto_villanos, (3 * self.ancho // 4 - texto_villanos.get_width() // 2, 150))

        iconos = list(iconos_jugadores.values())
        nombres_iconos = list(iconos_jugadores.keys())
        for i, icono in enumerate(iconos):
            pantalla.blit(icono, (50 + i * 200, self.alto // 2 - 75))
            nombre_icono = fuente.render(nombres_iconos[i], True, (255, 255, 255))
            pantalla.blit(nombre_icono, (50 + i * 200, self.alto // 2 + 100))

        # Dibujar recuadro amarillo alrededor del ícono seleccionado
        pygame.draw.rect(pantalla, (255, 255, 0), (50 + opcion_icono_seleccionada * 200 - 10, self.alto // 2 - 85, 170, 220), 5)

        pygame.display.flip()

    def pantalla_juego(self, pantalla, icono_jugador1, icono_jugador2, nombres_iconos, puntaje_jugador1, puntaje_jugador2, jugadores, iconos_jugadores):
        pantalla.fill((0, 0, 0))  # Limpiar la pantalla
        pantalla.blit(self.fondo_juego, ((self.ancho - self.fondo_juego.get_width()) // 2, (self.alto - self.fondo_juego.get_height()) // 2))  # Mostrar fondo del juego centrado
        fuente = pygame.font.Font(None, 100)  # Fuente más grande para los datos de los jugadores

        # Mostrar información del jugador 1
        if icono_jugador1:
            pantalla.blit(icono_jugador1, (self.ancho // 4 - 75, self.alto // 2 - 150))
            texto_nombre = fuente.render(f"{nombres_iconos[list(iconos_jugadores.values()).index(icono_jugador1)]}", True, (255, 255, 255))
            pantalla.blit(texto_nombre, (self.ancho // 4 - texto_nombre.get_width() // 2, self.alto // 2 + 50))
            texto_puntaje = fuente.render(f"Puntaje: {puntaje_jugador1}", True, (255, 255, 255))
            pantalla.blit(texto_puntaje, (self.ancho // 4 - texto_puntaje.get_width() // 2, self.alto // 2 + 150))

        # Mostrar información del jugador 2
        if jugadores == 2 and icono_jugador2:
            pantalla.blit(icono_jugador2, (3 * self.ancho // 4 - 75, self.alto // 2 - 150))
            texto_nombre = fuente.render(f"{nombres_iconos[list(iconos_jugadores.values()).index(icono_jugador2)]}", True, (255, 255, 255))
            pantalla.blit(texto_nombre, (3 * self.ancho // 4 - texto_nombre.get_width() // 2, self.alto // 2 + 50))
            texto_puntaje = fuente.render(f"Puntaje: {puntaje_jugador2}", True, (255, 255, 255))
            pantalla.blit(texto_puntaje, (3 * self.ancho // 4 - texto_puntaje.get_width() // 2, self.alto // 2 + 150))

        pygame.display.flip()