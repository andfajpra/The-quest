#----Aquí vamos a ir metiendo toda la configuración...

import pygame as pg

pg.init()

FUENTE_PRINCIPAL=pg.font.Font("the_quest/fuentes/Starjedi.ttf", 20)

FONDO= pg.image.load("the_quest/imagenes/fondo.png")
FONDO_MENU=pg.image.load("the_quest/imagenes/fondomenu.jpg")
FONDO_GAME_OVER=pg.image.load("the_quest/imagenes/game_over.png")

PLANETA=pg.image.load("the_quest/imagenes/planeta3.png")

EXPLOSION_SONIDO=pg.mixer.Sound("the_quest/sonidos/explosion.wav")

ANCHO = FONDO.get_width()
ALTO = FONDO.get_height()

#---Crear una ventana---
VENTANA=pg.display.set_mode((ANCHO, ALTO))



BLANCO = (255, 255, 255)
NEGRO = (0 ,0 ,0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 128, 0)
ROJO = (255, 0 ,0)
MAGENTA = (255, 0, 255)

FPS = 60
FPS2=90
CLOCK=pg.time.Clock()

## Definimos indices pantallas
MENU = 0
PARTIDA = 1
INSTRUCCIONES = 2
PUNTUACIONES = 3
WIN=4
GAME_OVER=5
FIN_JUEGO=6

##Definimos velocidades de nivel
VELOCIDAD_NIVEL= {
    1: [2,4],
    2: [4,6],
    3: [6,8] 
}



#Tiempo de nivel
TIEMPO_N1 = 20
TIEMPO_N2 = 40




#---Definimos tiempo máximo de partida---
TIEMPO_MAXIMO_PARTIDA=60
