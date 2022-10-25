#--Aquí crearemos el control del juego--

import pygame as pg
import the_quest
from the_quest import ANCHO, ALTO, MENU, PARTIDA, INSTRUCCIONES, PUNTUACIONES, WIN, GAME_OVER, FIN_JUEGO
from the_quest.pantallas import Game_over, Instrucciones, Menu, Partida, Puntuaciones, Win

class Controlador:
    def __init__(self):
        pantalla_principal = pg.display.set_mode((ANCHO, ALTO))
        metronomo = pg.time.Clock()
        
        self.pantallas = [Menu(pantalla_principal, metronomo), 
                          Partida(pantalla_principal, metronomo),
                          Instrucciones(pantalla_principal, metronomo),
                          Puntuaciones(pantalla_principal,metronomo),
                          Win(pantalla_principal,metronomo),
                          Game_over(pantalla_principal,metronomo)]

        
        self.pantalla = self.pantallas[MENU]

    def jugar(self):
            siguiente_pantalla = 0
            while siguiente_pantalla != FIN_JUEGO:
            #while bool(salida) == False:
                siguiente_pantalla = self.pantalla.bucle_ppal()
                if siguiente_pantalla != FIN_JUEGO:
                    self.pantalla = self.pantallas[siguiente_pantalla]
                #ix = (ix + 1) % len(self.pantallas) 
                
      