#---Aquí creamos los objetos que aparecerán en el juego---
import random
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

        #dimensiones nave
        self.ancho=75
        self.alto=75
        
        self.vx = 0
        self.vy = 0

        self.vida=100


    
    def dibujar(self,pantalla):
        pantalla.blit(self.imagen,(self.rectangulo.x, self.rectangulo.y)) #para dibujar la nave con sus coordenadas
    
    
    def mover(self, tecla_arriba, tecla_abajo, y_max=470): #el y_max es para limitar el máximo de la pantalla. De momento tenemos 475
        estado_teclas=pg.key.get_pressed()  #key es la libreria del pygame, get_pressed() es una funcion, que me devuelve una lista de 512 teclas(elementos), si la tecla esta a True --> la tecla esta pulsada 
        if estado_teclas[tecla_arriba]:   #si esta tecla está pulsada, me aplicas la velocidad de y en formato negativo (para arriba es negativo)
            self.rectangulo.y -=self.vy

        if self.rectangulo.y < 0 + self.alto //2:    #ponemos el límite de arriba de pantalla
            self.rectangulo.y = self.alto //2

        if estado_teclas[tecla_abajo]:  #si esta tecla está pulsada, me aplicas la velocidad de y en formato positivo (para abajo es positivo)
            self.rectangulo.y += self.vy                               

        if self.rectangulo.y > y_max - self.alto//2:  #ponemos el límite de abajo
            self.rectangulo.y = y_max - self.alto //2

        @property
        def izquierda(self):
            return self.rectangulo.x - self.ancho //2

        @property
        def derecha(self):
         return self.rectangulo.x + self.ancho // 2

        @property
        def arriba(self):
            return self.rectangulo.y - self.ancho // 2

        @property
        def abajo(self):
            return self.rectangulo.y + self.ancho //2

        #---Teclas derecha izquierda---

        
    def moverlateral(self, tecla_izquierda, tecla_derecha, x_max=800):
        estado_teclas=pg.key.get_pressed()  
        if estado_teclas[tecla_izquierda]:   
            self.rectangulo.x -=self.vx

        if self.rectangulo.x < 0 + self.ancho //2:    
            self.rectangulo.x = self.ancho //2

        if estado_teclas[tecla_derecha]:  
            self.rectangulo.x += self.vx                               

        if self.rectangulo.x > x_max - self.ancho//2:  
            self.rectangulo.x = x_max - self.ancho //2

    def disparar(self):
        bala=Balas(self.rectangulo.y,self.rectangulo.top) #esto es un objeto de la clase Balas que creamos abajo. Le pasamos coordenadas.
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()


class Obstaculo:
    def __init__(self):
        self.imagen=pg.image.load("the_quest/imagenes/asteroid1.png").convert_alpha()
        self.rectangulo=self.imagen.get_rect()
        self.rectangulo.x=random.randrange(1,ANCHO+5)
        self.rectangulo.y=10
        self.velocidad_y=random.randrange(-5,20)

    def dibujar(self,pantalla):
        pantalla.blit(self.imagen,(self.rectangulo.x, self.rectangulo.y)) 

    def actualizar(self):
        self.time=random.randrange(-1, pg.time.get_ticks()//5000) #get_ticks tiempo transcurrido desde que iniciamos juego, va aumentando el tiempo
        self.rectangulo.x +=self.time
        if self.rectangulo.x >=ANCHO:  #cuando la poscion de x sea mayor q el ancho de x lo iniciamos de nuevo en cero
            self.rectangulo.x=835
            self.rectangulo.y -=50

    

class Balas(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.imagen = pg.image.load("the_quest/imagenes/explosion1.png").convert_alpha()
        self.rectangulo=self.imagen.get_rect()
        self.rectangulo.x=x
        self.rectangulo.y=y
        self.velocidad= 18

    def dibujar(self,pantalla):
        pantalla.blit(self.imagen,(self.rectangulo.x, self.rectangulo.y)) 

    def actualizar(self):
        self.rectangulo.x += self.velocidad
        if self.rectangulo.bottom <0:
            self.kill()   #elimina grupo_jugador creados. elimina los elementos de esa lista.


#class Balas_obstaculos(pg.sprite.Sprite):


class Explosion(pg.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()



grupo_jugador=pg.sprite.Group()
grupo_balas_jugador=pg.sprite.Group()





    