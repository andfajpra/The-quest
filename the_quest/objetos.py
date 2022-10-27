#---Aquí creamos los objetos que aparecerán en el juego---
from genericpath import exists
import random
from re import X
import time
import pygame as pg
from the_quest import ANCHO, ALTO, PLANETA, PUNTUACIONES
import sqlite3

class Nave(pg.sprite.Sprite):
    

    def __init__(self):
        super().__init__()
        self.image=pg.image.load("the_quest/imagenes/craft4.png").convert_alpha()#lo convertimos a alpha para eliminar el fondo
        self.image=pg.transform.scale(self.image,(75,75))
        pg.display.set_icon(self.image) #esto es para colocar esta misma imagen como icono del juego
        self.rect=self.image.get_rect() #Vamos a posicionar el rectángulo que utiliza la imagen

        #ahora posicionamos la nave
        self.rect.x=4
        self.rect.y=ALTO//2
       

        #dimensiones nave
        self.ancho=75
        self.alto=75
        
        self.vx = 5
        self.vy = 5


        #Vbles para rotación
        self.rotando=False
        self.angulo=0        
        self.imagen_rotacion=pg.image.load("the_quest/imagenes/craft4.png").convert_alpha()
        self.imagen_rotacion=pg.transform.scale(self.image,(75,75))

    
    def draw(self,pantalla):
        pantalla.blit(self.image,(self.rect.x, self.rect.y)) #para dibujar la nave con sus coordenadas
    
    
    def update(self, y_max=ALTO-75): #el y_max es para limitar el máximo de la pantalla. De momento tenemos 475
        estado_teclas=pg.key.get_pressed()  #key es la libreria del pygame, get_pressed() es una funcion, que me devuelve una lista de 512 teclas(elementos), si la tecla esta a True --> la tecla esta pulsada 
        if estado_teclas[pg.K_UP]:   #si esta tecla está pulsada, me aplicas la velocidad de y en formato negativo (para arriba es negativo)
            self.rect.y -=self.vy

        if self.rect.y < 0: # + self.alto //2:    #ponemos el límite de arriba de pantalla
            self.rect.y = 0 #self.alto //2

        if estado_teclas[pg.K_DOWN]:  #si esta tecla está pulsada, me aplicas la velocidad de y en formato positivo (para abajo es positivo)
            self.rect.y += self.vy                               

        if self.rect.y > y_max: # - self.alto//2:  #ponemos el límite de abajo
            self.rect.y = y_max # - self.alto //2

        @property
        def izquierda(self):
            return self.rect.x - self.ancho //2

        @property
        def derecha(self):
            return self.rect.x + self.ancho // 2

        @property
        def arriba(self):
            return self.rect.y - self.ancho // 2

        @property
        def abajo(self):
            return self.rect.y + self.ancho //2

        

    def disparar(self):
        bala=Balas(self.rect.centery,self.rect.right) #esto es un objeto de la clase Balas que creamos abajo. Le pasamos coordenadas.
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()

    def mov_lateral(self,x_max=630):
        self.vx=1

        if self.rect.x < x_max:
            if self.rect.centery<ALTO//2:
                self.rect.centery +=1
            elif self.rect.centery>ALTO//2:
                self.rect.centery -=1
            self.rect.x +=self.vx
        else:
            self.rotacion_nave()


    def rotacion_nave(self):
        
        print("rotando",self.rotando)
        print("angulo", self.angulo)
        old_center = self.rect.center

        if self.rotando: #si rotando es igual a True
            self.angulo += 1
            angulo_rotacion=(self.angulo)/2
            self.image=pg.transform.rotate(self.imagen_rotacion, angulo_rotacion)
            self.rect = self.image.get_rect(center=old_center)

            if angulo_rotacion==180:
                self.image180 = self.image
                self.rotando=False

        else:
            self.ancho -= 1
            self.alto -=1
            self.image = pg.transform.scale(self.image180, (self.ancho, self.alto))
            self.rect = self.image.get_rect(center=old_center)

        
       


class Obstaculo(pg.sprite.Sprite):
    def __init__(self,velocidad):
        super().__init__()
        self.image=pg.image.load("the_quest/imagenes/asteroid.png").convert_alpha()
        #tamano_escala=random.randrange(10, self.image.get_width())
        tamano_escala=random.randrange(10,90)
        self.image=pg.transform.scale(self.image,(tamano_escala,tamano_escala))
        self.rect=self.image.get_rect()
        self.rect.x=random.randrange(ANCHO + 10, ANCHO + 70)
        self.rect.y=random.randrange(ALTO-self.rect.height)
        #self.velocidad_x=random.randrange(pg.time.get_ticks()//5000 + 5) #úmero de pixeles que me voy a desplazar en x
        self.velocidad_x=random.randrange(velocidad[0],velocidad[1])
        self.superado = 0

    def draw(self,pantalla):
        pantalla.blit(self.image,(self.rect.x, self.rect.y)) 

    def update(self):
        #self.velocidad_x=random.randrange(pg.time.get_ticks()//8000 + 1 )#get_ticks tiempo transcurrido desde que iniciamos juego, va aumentando el tiempo
        self.rect.x -= self.velocidad_x
        self.superado = 0
        #self.rect.x -= self.velocidad_x
        if self.rect.x <=0:  #cuando la poscion de x sea mayor q el ancho de x lo iniciamos de nuevo en cero
            #time.sleep(random.randrange(1, 5))
            self.rect.x=random.randrange(ANCHO + 10, ANCHO + 70)
            self.rect.y=random.randrange(ALTO-self.rect.height)
            self.superado = 1
    
    def cambia_velocidad(self, velocidad):
        self.velocidad_x=random.randrange(velocidad[0],velocidad[1])

    

    

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
        if self.rectangulo.right >835:
            self.kill()   #elimina grupo_jugador creados. elimina los elementos de esa lista.





class Explosion(pg.sprite.Sprite):
    def __init__(self, posicion, lista_explosion):
        super().__init__()
        self.lista_explosion=lista_explosion
        self.image=lista_explosion[0]
        self.image=pg.transform.scale(self.image, (75,75))
        self.rect=self.image.get_rect()
        self.rect.center=posicion
        self.tiempo_ultimo=pg.time.get_ticks() #me da el tiempo desde el inicio
        self.tiempo_explosion=50
        self.indice_imagen=0

    def update(self):
        tiempo_actual=pg.time.get_ticks() #esto me da el tiempo desde l inicio
        if tiempo_actual-self.tiempo_ultimo > self.tiempo_explosion: #si ha pasado entre el tiempo actual y el ultimo 30 (self.tiempo_explosion)
            self.tiempo_ultimo = tiempo_actual #actualizo el tiempo ultimo al tiempo actual
            self.indice_imagen += 1
            if self.indice_imagen == len(self.lista_explosion):
                self.kill()  #matamos la explosion
            else:
                posicion= self.rect.center
                self.image=self.lista_explosion[self.indice_imagen]
                self.image=pg.transform.scale(self.image, (70,70))
                self.rect=self.image.get_rect()
                self.rect.center=posicion

        

class Planeta(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=PLANETA.convert_alpha()#lo convertimos a alpha para eliminar el fondo
        self.image=pg.transform.scale(self.image,(200,200))
        
        self.rect=self.image.get_rect() #Vamos a posicionar el rectángulo que utiliza la imagen

        #ahora posicionamos el planeta
        self.rect.centerx=ANCHO+5
        self.rect.centery=ALTO//2

    def draw(self,pantalla):
        pantalla.blit(self.image,(self.rect.x, self.rect.y))

    def update(self, x_min=600):
        if self.rect.x > x_min:
            self.rect.x -= 1
        
       
       



class Bbdd():
    #Creamos BBDD y tabla
    def __init__(self):
        self.con=sqlite3.connect("the_quest/bbdd/records.db")
        self.cur=self.con.cursor()
        self.cur.execute('''CREATE TABLE if not exists "records" (
	                     "iniciales"	TEXT NOT NULL,
	                     "puntuaciones"	INTEGER
                         )''')
        self.con.commit()
        


    #Creamos consulta en orden 3 primeras puntuaciones
    def select(self):
        
        consulta= 'SELECT * FROM records order by puntuaciones DESC limit 3'
        
        self.cur.execute(consulta)
        datos=self.cur.fetchall()

        return datos
    
    #Función para insertar puntuación

    def inserta_puntuacion(self, puntuaciones, iniciales):

        consulta=f'insert into records (iniciales, puntuaciones) values ("{iniciales}", "{puntuaciones}")'
        self.cur.execute(consulta)
        self.con.commit()


    def cerrar_conexion(self):

        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()







