#----Aquí vamos a ir metiendo toda la configuración...
import pygame as pg
pg.init()


FONDO= pg.image.load("the_quest/imagenes/fondo.png")

ANCHO = FONDO.get_width()
ALTO = FONDO.get_height()
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
