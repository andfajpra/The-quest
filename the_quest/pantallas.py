#---Aquí crearemos las partidas y las distintas pantallas con el menú de inicio---

import pygame as pg
from the_quest.objetos import Nave, Obstaculo, Balas
from the_quest import ANCHO, ALTO, BLANCO, NARANJA, MAGENTA,NEGRO,FPS, FONDO
from random import random

class Partida:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("THE QUEST")

        self.nave=Nave()
        self.obstaculo=Obstaculo()
        self.balas=Balas(75//2,75//2)

        
        self.nave.vy=5
        self.nave.vx=5


        #self.fuenteMarcador = pg.font.Font("pong/fonts/silkscreen.ttf", 40)
        #self.fuenteTemporizador = pg.font.Font("pong/fonts/silkscreen.ttf", 20)

        self.contadorFotogramas = 0
        self.fondoPantalla = FONDO



    def bucle_ppal(self):
        
        #self.puntuacion1 = 0
        #self.puntuacion2 = 0
        #self.temporizador = TIEMPO_MAXIMO_PARTIDA

        game_over = False
        self.metronomo.tick()
        while not game_over:

            """""
            and \
              self.puntuacion1 < PUNTUACION_GANADORA and \
              self.puntuacion2 < PUNTUACION_GANADORA and \
              self.temporizador > 0:
            """
            salto_tiempo = self.metronomo.tick(FPS)
            
            #self.temporizador -= salto_tiempo

            for evento in pg.event.get():
                if evento.type == pg.QUIT: #pg.QUIT es cuando le damos a la x de la ventana
                    return True
        
            

            self.nave.mover(pg.K_UP, pg.K_DOWN)
            self.nave.moverlateral(pg.K_LEFT,pg.K_RIGHT)
            self.obstaculo.actualizar()
            self.balas.actualizar() 


            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
    

            self.nave.dibujar(self.pantalla_principal)
            self.obstaculo.dibujar(self.pantalla_principal)
            self.balas.dibujar(self.pantalla_principal)

            """ 
            p1 = self.fuenteMarcador.render(str(self.puntuacion1), True, BLANCO)
            p2 = self.fuenteMarcador.render(str(self.puntuacion2), True, BLANCO)
            contador = self.fuenteTemporizador.render(str(self.temporizador / 1000), True, BLANCO)

            self.pantalla_principal.blit(p1,(10,10))
            self.pantalla_principal.blit(p2, (ANCHO - 45, 10))
            self.pantalla_principal.blit(contador, (ANCHO // 2, 10)) """

            pg.display.flip()


class Menu:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("Menu")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuenteComenzar= pg.font.Font("the_quest/fuentes/fast99.ttf",50)
        #self.musica= pg.mixer.Sound("")
    
    def bucle_ppal(self):
        game_over = False
        

        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True

                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_RETURN:
                        game_over = True

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            menu = self.fuenteComenzar.render("Pulsa ENTER para comenzar", True, MAGENTA)
            self.pantalla_principal.blit(menu, (50, ALTO //2))
            pg.display.flip()

        #self.musica.stop()
        