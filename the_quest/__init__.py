#----Aquí vamos a ir metiendo toda la configuración...
import pygame as pg
pg.init()


FONDO= pg.image.load("the_quest/imagenes/fondo.png")
FONDO_GAME_OVER=pg.image.load("the_quest/imagenes/game_over.png")
FONDO_PLANETA=pg.image.load("the_quest/imagenes/planeta_1.png")

ANCHO = FONDO.get_width()
ALTO = FONDO.get_height()

#---Crear una ventana---
VENTANA=pg.display.set_mode((ANCHO, ALTO))

#SONIDO_GOLPE=pygame.mixer.Sound("")

BLANCO = (255, 255, 255)
NEGRO = (0 ,0 ,0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 128, 0)
ROJO = (255, 0 ,0)
MAGENTA = (255, 0, 255)

FPS = 60
CLOCK=pg.time.Clock()

## Definimos indices pantallas
MENU = 0
PARTIDA = 1
INSTRUCCIONES = 2
PUNTUACIONES = 3
WIN=4
GAME_OVER=5
FIN_JUEGO=6


#---Definimos puntuación ganadora y tiempo máximo de partida---
TIEMPO_MAXIMO_PARTIDA=10
