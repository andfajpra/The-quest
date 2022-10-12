#---Aquí creamos los objetos que aparecerán en el juego---
import pygame as pg
from the_quest import ANCHO, ALTO

class Nave:
    

    def __init__(self):
        self.imagen=pg.image.load("the_quest/imagenes/craft.png").convert_alpha() #lo convertimos a alpha para eliminar el fondo
        pg.display.set_icon(self.imagen) #esto es para colocar esta misma imagen como icono del juego
        self.rectangulo=self.imagen.get_rect() #convertimos imagen a rectángulo

        #ahora posicionamos la nave
        self.rectangulo.x=5
        self.rectangulo.y=ALTO//2-75//2
        
        self.vx = 0
        self.vy = 0

        self.vida=100


    
    def dibujar(self,pantalla):
        pantalla.blit(self.imagen,(self.rectangulo.x, self.rectangulo.y)) #para dibujar la nave con sus coordenadas
    
    """"
    def mover(self, tecla_arriba, tecla_abajo, y_max=600): #el y_max es para informarle a la raqueta que es el límite que tiene
        estado_teclas=pg.key.get_pressed()  #key es la libreria del pygame, get_pressed() es una funcion, que me devuelve una lista de 512 teclas(elementos), si la tecla esta a True --> la tecla esta pulsada 
        if estado_teclas[tecla_arriba]:   #si esta tecla está pulsada, me aplicas la velocidad de y en formato negativo (para arriba es negativo)
            self.y -= self.vy                                #raqueta2.center_y -=raqueta2.vy


        if self.y < 0 + self.h //2:    #ponemos el límite de arriba de pantalla
            self.y = self.h //2

        if estado_teclas[tecla_abajo]:  #si esta tecla está pulsada, me aplicas la velocidad de y en formato positivo (para abajo es positivo)
            self.y += self.vy                               

        if self.y > y_max - self.h //2:  #ponemos el límite de abajo
            self.y = y_max - self.h //2

        @property
        def izquierda(self):
            return self.x - self.w //2

        @property
        def derecha(self):
         return self.x + self.w // 2

        @property
        def arriba(self):
            return self.y - self.h // 2

        @property
        def abajo(self):
            return self.y + self.h //2

       """