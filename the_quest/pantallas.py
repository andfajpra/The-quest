#---Aquí crearemos las partidas y las distintas pantallas con el menú de inicio---

import pygame as pg
from the_quest.objetos import Explosion, Nave, Obstaculo, Balas
from the_quest import ANCHO, ALTO, BLANCO, NARANJA, MAGENTA,NEGRO,FPS, FONDO
from random import random

class Partida:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("THE QUEST")

        self.nave=Nave()

        self.grupo_obstaculos = pg.sprite.Group() #creo el grupo obstaculo
        self.balas=Balas(self.nave.rect.centerx,self.nave.rect.centery)
        self.all_sprites=pg.sprite.Group()

        self.all_sprites.add(self.nave)  #para actualizar todos los sprites a  la vez
        
        self.n_vidas=3


        self.fuente_vidas = pg.font.Font("the_quest/fuentes/fast99.ttf", 30)
        #self.fuenteTemporizador = pg.font.Font("pong/fonts/silkscreen.ttf", 20)

        self.contadorFotogramas = 0
        self.fondoPantalla = FONDO

        #--Creo 10 objetos obstaculos--
        for i in range(10):
            obstaculo=Obstaculo() #creo un objeto obstaculo
            self.grupo_obstaculos.add(obstaculo) #para comprobar colisiones
            self.all_sprites.add(obstaculo) #para actualizar todos los sprites a la vez

        #--Creo la lista de explosiones que utilizaré en el metodo update de la clase Explosion---
        self.lista_explosion=[]
        for i in range(1,13):
            explosion = pg.image.load(f'the_quest/imagenes/explosion/{i}.png')
            self.lista_explosion.append(explosion)

    def bucle_ppal(self):
        
        #self.puntuacion1 = 0
        #self.puntuacion2 = 0
        #self.temporizador = TIEMPO_MAXIMO_PARTIDA


        game_over = False
        self.metronomo.tick()
        while not game_over and self.n_vidas > 0:

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
        
            

            #self.nave.update(pg.K_UP, pg.K_DOWN)
            #self.grupo_obstaculos.update()
            self.all_sprites.update()
            self.balas.actualizar() 

            #-----Colision nave-meteorito----
            colisiones=pg.sprite.spritecollide(self.nave,self.grupo_obstaculos,True) #comprobamos colision entre nave y alguno de los obstáculos del grupo
            for colision in colisiones:
                explosion=Explosion(self.nave.rect.center,self.lista_explosion)
                self.n_vidas -=1  #reestamos vida
                obstaculo=Obstaculo()  #creo obstaculo nuevo
                self.grupo_obstaculos.add(obstaculo) #lo añado al grupo de obstaculos
                self.all_sprites.add(obstaculo)  #lo añado al grupo all sprites
                self.all_sprites.add(explosion) #la explosion la añado al grupo all sprites



            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
    

            #self.nave.draw(self.pantalla_principal)
            #self.grupo_obstaculos.draw(self.pantalla_principal)
            self.all_sprites.draw(self.pantalla_principal)
            self.balas.dibujar(self.pantalla_principal)

            vidas = self.fuente_vidas.render(str(self.n_vidas), True, BLANCO)
            #contador = self.fuenteTemporizador.render(str(self.temporizador / 1000), True, BLANCO)

            self.pantalla_principal.blit(vidas,(10,10))
            #self.pantalla_principal.blit(p2, (ANCHO - 45, 10))
            #self.pantalla_principal.blit(contador, (ANCHO // 2, 10))

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
        