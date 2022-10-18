#---Aquí crearemos las partidas y las distintas pantallas con el menú de inicio---

from cmath import rect
import pygame as pg
from the_quest.objetos import Explosion, Nave, Obstaculo, Balas
from the_quest import ANCHO, ALTO, BLANCO, NARANJA, MAGENTA,NEGRO,FPS, FONDO, TIEMPO_MAXIMO_PARTIDA
from the_quest import MENU, PARTIDA, INSTRUCCIONES, PUNTUACIONES, WIN, GAME_OVER, FIN_JUEGO
from random import random
import pygame.font
from time import time

texto_historia1= """La busqueda comienza en un planeta tierra moribundo"""
texto_historia2="""por el cambio climático. Partiremos a la búsqueda de"""
texto_historia3="""un planeta compatible con la vida humana para colonizarlo"""


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


        self.fuente_vidas = pg.font.Font("the_quest/fuentes/fast99.ttf", 30)
        self.fuenteTemporizador = pg.font.Font("the_quest/fuentes/fast99.ttf", 20)

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
        
        self.puntuacion_tiempo = 0
        self.puntuacion_obstaculos = 0
        self.temporizador = 0
        self.t_start = time()
        self.n_vidas = 3



        #game_over = False
        #self.metronomo.tick()
        while self.n_vidas > 0 and self.temporizador<TIEMPO_MAXIMO_PARTIDA:

            salto_tiempo = self.metronomo.tick(FPS) #los milisegundos que han pasado entre frame y frame
            
            # Calculamos el tiempo desde el inicio del bucle principal
            self.temporizador = time() - self.t_start


            for evento in pg.event.get():
                if evento.type == pg.QUIT: #pg.QUIT es cuando le damos a la x de la ventana
                    #return True
                    return FIN_JUEGO
        
        
            

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

            # Por cada segundo sumamos 10 puntos
            self.puntuacion_tiempo = 10 * int(self.temporizador)
            # Comprobamos si hemos superado algun obstaculo, si es asi sumamos otros 10 puntos
            for obstaculo in self.grupo_obstaculos:
                self.puntuacion_obstaculos += 10 * obstaculo.superado


            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
    

            #self.nave.draw(self.pantalla_principal)
            #self.grupo_obstaculos.draw(self.pantalla_principal)
            self.all_sprites.draw(self.pantalla_principal)
            self.balas.dibujar(self.pantalla_principal)

            vidas = self.fuente_vidas.render(str(self.n_vidas), True, BLANCO)
            contador = self.fuenteTemporizador.render(str(round(self.temporizador, 2)), True, BLANCO)
            puntuacion = self.fuenteTemporizador.render(str(self.puntuacion_tiempo + self.puntuacion_obstaculos), True, BLANCO)

            self.pantalla_principal.blit(vidas,(10,10))
            self.pantalla_principal.blit(contador, (ANCHO // 2, 10))
            self.pantalla_principal.blit(puntuacion, (ANCHO - 40, 10))

            pg.display.flip()

        if self.n_vidas == 0:
            return GAME_OVER
        else:
            return WIN


class Menu:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        #pg.display.set_caption("Menu")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_menu= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        self.fuente_nombre_juego=pg.font.Font("the_quest/fuentes/fast99.ttf",60)
        self.fuente_titulo_historia=pg.font.Font("the_quest/fuentes/fast99.ttf",15)
        self.fuente_historia=pg.font.Font("the_quest/fuentes/fast99.ttf",15)
        self.fuente_puntuaciones=pg.font.Font("the_quest/fuentes/fast99.ttf",20)
       

        #self.musica= pg.mixer.Sound("") buscar música para meterle
    
    def bucle_ppal(self):
        pg.display.set_caption("Menu")
        game_over = False
        
        #self.musica.play(-1)
        
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return FIN_JUEGO

                if evento.type == pg.KEYDOWN: 
                    if evento.key == pg.K_RETURN:
                        return PARTIDA
                    if evento.key == pg.K_i:
                        return INSTRUCCIONES
                    if evento.key == pg.K_p:
                        return PUNTUACIONES
                    

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            nombre_juego=self.fuente_nombre_juego.render("THE QUEST", True, BLANCO)
            titulo_historia=self.fuente_titulo_historia.render("Historia del juego:", True, BLANCO)
            historia=self.fuente_historia.render(texto_historia1,True,BLANCO)
            historia2=self.fuente_historia.render(texto_historia2,True,BLANCO)
            historia3=self.fuente_historia.render(texto_historia3,True,BLANCO)
            menu = self.fuente_menu.render("*Pulsa ENTER para comenzar", True, BLANCO)
            instrucciones= self.fuente_menu.render("*Pulsa i para ver las instrucciones", True, BLANCO)
            puntuaciones= self.fuente_puntuaciones.render("*Pulsa p para ver las puntuaciones", True, BLANCO)
            self.pantalla_principal.blit(nombre_juego, (100, 10))
            self.pantalla_principal.blit(titulo_historia, (100, 70))
            self.pantalla_principal.blit(historia, (100,90))
            self.pantalla_principal.blit(historia2, (100,105))
            self.pantalla_principal.blit(historia3, (100,120))
            self.pantalla_principal.blit(menu, (400, ALTO -100))
            self.pantalla_principal.blit(instrucciones, (400, ALTO -200))
            self.pantalla_principal.blit(puntuaciones, (400, ALTO -300))
            pg.display.flip()

        #self.musica.stop()


class Instrucciones:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("Instrucciones")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_instrucciones= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        

    def bucle_ppal(self):
        game_over = False
        #self.musica.play(-1)
        
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return FIN_JUEGO

                if evento.type == pg.KEYDOWN: 
                    if evento.key == pg.K_ESCAPE:
                        return MENU
            

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            instrucciones=self.fuente_instrucciones.render("Instrucciones:", True, BLANCO)
            
            self.pantalla_principal.blit(instrucciones, (100, 70))
            
            
            pg.display.flip()


class Puntuaciones:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("Puntuaciones")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_puntuaciones= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        

    def bucle_ppal(self):
        game_over = False
        #self.musica.play(-1)
        
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return FIN_JUEGO

                
                if evento.type == pg.KEYDOWN: 
                    if evento.key == pg.K_ESCAPE:
                        return MENU
    
            

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            puntuaciones=self.fuente_puntuaciones.render("Puntuaciones:", True, BLANCO)
            
            self.pantalla_principal.blit(puntuaciones, (100, 70))
            
            
            pg.display.flip()

class Win:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("WIN")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_win= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        

    def bucle_ppal(self):
        game_over = False
        #self.musica.play(-1)
        
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return FIN_JUEGO

                
                if evento.type == pg.KEYDOWN: 
                    if evento.key == pg.K_ESCAPE:
                        return MENU
    
            

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            win=self.fuente_win.render("¡¡¡ENHORABUENA!!! HAS GANADO! Pulsa Escape para volver al inicio", True, BLANCO)
            
            self.pantalla_principal.blit(win, (100, 70))
            
            
            pg.display.flip()

class Game_over:
    def __init__(self, pantalla, metronomo):
        self.pantalla_principal = pantalla
        self.metronomo = metronomo
        pg.display.set_caption("GAME OVER")
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_win= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        

    def bucle_ppal(self):
        game_over = False
        #self.musica.play(-1)
        
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return FIN_JUEGO

                
                if evento.type == pg.KEYDOWN: 
                    if evento.key == pg.K_ESCAPE:
                        return MENU
    
            

            self.pantalla_principal.blit(self.imagenFondo, (0, 0))
            win=self.fuente_win.render("¡¡¡GAME_OVER!!!  Pulsa Escape para volver al inicio", True, BLANCO)
            
            self.pantalla_principal.blit(win, (100, 70))
            
            
            pg.display.flip()

