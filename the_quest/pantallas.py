#---Aquí crearemos las partidas y las distintas pantallas con el menú de inicio---

from cmath import rect
import pygame as pg
from the_quest.objetos import Bbdd, Explosion, Nave, Obstaculo, Balas
#from the_quest import ANCHO, ALTO, BLANCO, FONDO_GAME_OVER, FONDO_PLANETA, NARANJA, MAGENTA,NEGRO,FPS, FONDO, PLANETA, TIEMPO_MAXIMO_PARTIDA
#from the_quest import MENU, PARTIDA, INSTRUCCIONES, PUNTUACIONES, WIN, GAME_OVER, FIN_JUEGO
from the_quest import *
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


        self.fuente_vidas = pg.font.Font("the_quest/fuentes/fast99.ttf", 30)
        self.fuenteTemporizador = pg.font.Font("the_quest/fuentes/fast99.ttf", 20)
        self.fuenteNivel = pg.font.Font("the_quest/fuentes/fast99.ttf", 20)
        self.fondoPantalla = FONDO
        

        #--Creo la lista de explosiones que utilizaré en el metodo update de la clase Explosion---
        self.lista_explosion=[]
        for i in range(1,13):
            explosion = pg.image.load(f'the_quest/imagenes/explosion/{i}.png')
            self.lista_explosion.append(explosion)

    def bucle_ppal(self):
        
        pg.display.set_caption("THE QUEST")

        self.nivel=1
        self.nave=Nave()

        self.grupo_obstaculos = pg.sprite.Group() #creo el grupo obstaculo
        self.balas=Balas(self.nave.rect.centerx,self.nave.rect.centery)
        self.all_sprites=pg.sprite.Group()

        self.all_sprites.add(self.nave)  #para actualizar todos los sprites a  la vez

        #--Creo 5 objetos obstaculos para Nivel 1--
        self.add_obstaculos(4)

        self.contadorFotogramas = 0
        self.puntuacion_tiempo = 0
        self.puntuacion_obstaculos = 0
        self.temporizador = 0
        self.t_start = time()
        self.n_vidas = 3
        self.bbdd=Bbdd()

        
        #----Bucle PARTIDA---:
        while self.n_vidas > 0 and self.temporizador<TIEMPO_MAXIMO_PARTIDA:

            salto_tiempo = self.metronomo.tick(FPS) #los milisegundos que han pasado entre frame y frame
            
            # Calculamos el tiempo desde el inicio del bucle principal
            self.temporizador = time() - self.t_start

            #Hacemos el check nivel para ver en que nivel estamos
            self.check_nivel()


            for evento in pg.event.get():
                if evento.type == pg.QUIT: #pg.QUIT es cuando le damos a la x de la ventana
                    #return True
                    self.bbdd.cerrar_conexion()
                    return FIN_JUEGO

            self.all_sprites.update()
            self.balas.actualizar() 

            #-----Colision nave-meteorito----
            colisiones=pg.sprite.spritecollide(self.nave,self.grupo_obstaculos,True) #comprobamos colision entre nave y alguno de los obstáculos del grupo
            for colision in colisiones:
                explosion=Explosion(self.nave.rect.center,self.lista_explosion)
                self.n_vidas -=1  #reestamos vida
                obstaculo=Obstaculo(VELOCIDAD_NIVEL[self.nivel])  #creo obstaculo nuevo
                self.grupo_obstaculos.add(obstaculo) #lo añado al grupo de obstaculos
                self.all_sprites.add(obstaculo)  #lo añado al grupo all sprites
                self.all_sprites.add(explosion) #la explosion la añado al grupo all sprites

            # Por cada segundo sumamos 10 puntos
            self.puntuacion_tiempo = 10 * int(self.temporizador)
            # Comprobamos si hemos superado algun obstaculo, si es asi sumamos otros 10 puntos
            for obstaculo in self.grupo_obstaculos:
                self.puntuacion_obstaculos += 10 * obstaculo.superado


            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
        
            self.all_sprites.draw(self.pantalla_principal)
            self.balas.dibujar(self.pantalla_principal)

            vidas = self.fuente_vidas.render(f'Vidas: {self.n_vidas}', True, BLANCO)
            contador = self.fuenteTemporizador.render(f'{round(self.temporizador, 2)}', True, BLANCO)
            puntuacion = self.fuenteTemporizador.render(str(self.puntuacion_tiempo + self.puntuacion_obstaculos), True, BLANCO)
            nivel= self.fuenteNivel.render(f'Nivel: {self.nivel}',True,BLANCO)

            self.pantalla_principal.blit(vidas,(10,10))
            self.pantalla_principal.blit(contador, (ANCHO // 2, 10))
            self.pantalla_principal.blit(puntuacion, (ANCHO - 40, 10))
            self.pantalla_principal.blit(nivel, (ANCHO -100, 30))

            pg.display.flip()

        if self.n_vidas == 0:
            print("Entra aqui. vidas:", self.n_vidas)
            if self.comprueba_puntuacion() ==1:
                iniciales = self.get_iniciales()
                self.bbdd.inserta_puntuacion(self.puntuacionfinal,iniciales)
                #self.muestra_puntuacion()
            self.bbdd.cerrar_conexion()
            return GAME_OVER
        else:
            print(self.grupo_obstaculos.has())
            self.nave.rotando=True
            while len(self.grupo_obstaculos.sprites())>1 or self.nave.rotando==True:
            #---Bucle Final.....
                self.grupo_obstaculos.update()
                self.nave.mov_lateral()
                print(len(self.grupo_obstaculos.sprites()))
                print(self.grupo_obstaculos.sprites())
                for obstaculo in self.grupo_obstaculos:
                    if obstaculo.superado==1:
                        obstaculo.kill()
                self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
                self.all_sprites.draw(self.pantalla_principal)
                self.pantalla_principal.blit(vidas,(10,10))
                self.pantalla_principal.blit(contador, (ANCHO // 2, 10))
                self.pantalla_principal.blit(puntuacion, (ANCHO - 40, 10))

                pg.display.flip()

            
            if self.comprueba_puntuacion() == 1:
                iniciales = self.get_iniciales()
                self.bbdd.inserta_puntuacion(self.puntuacionfinal,iniciales)
                self.muestra_puntuacion()
            
            self.bbdd.cerrar_conexion()

            return WIN

    def comprueba_puntuacion(self):
        #---Comprobamos puntuaciones
        self.puntuacionfinal=self.puntuacion_obstaculos + self.puntuacion_tiempo #mi puntuacion es la suma de estas dos

        mejores3=self.bbdd.select() #ejecutamos consulta creada select

        if len(mejores3)==0: #si la longitud es cero
            return 1   #la mía será mejor

        es_mejor = 0 #bandera
        
        for i, p in mejores3:  #la consulta me da una lista de tuplas con iniciales (i) y puntuaciones (p)
            if self.puntuacionfinal >= p: #si mi puntuacion final es mejor que alguna de las p anteriores
                es_mejor = 1            #la bandera se pone a 1
                break

        return es_mejor


    def get_iniciales(self):
        
        casilla_iniciales = pg.Rect(100, 100, 140, 32)
        iniciales = ''
        fin_iniciales = False

        while not fin_iniciales:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.bbdd.cerrar_conexion()
                    return FIN_JUEGO
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        print(iniciales)
                        fin_iniciales = True
                    elif event.key == pg.K_BACKSPACE:
                        iniciales = iniciales[:-1]
                    else:
                        iniciales += event.unicode

            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))
            # Render the current text.
            texto_iniciales = self.fuente_vidas.render(f'Introduce tus iniciales: {iniciales}', True, BLANCO)
            # Resize the box if the text is too long.
            width = max(200, texto_iniciales.get_width()+10)
            casilla_iniciales.w = width
            # Blit the text.
            self.pantalla_principal.blit(texto_iniciales, (casilla_iniciales.x+5, casilla_iniciales.y+5))
            # Blit the input_box rect.
            #pg.draw.rect(screen, color, input_box, 2)

            pg.display.flip()
        
        return iniciales
            
            
    def muestra_puntuacion(self):

        mejores3=self.bbdd.select() #ejecutamos consulta creada select

       
        fin_iniciales = False

        while not fin_iniciales:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.bbdd.cerrar_conexion()
                    return FIN_JUEGO
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        fin_iniciales = True
                    

            self.pantalla_principal.blit(self.fondoPantalla, (0, 0))

            iniciales = self.fuente_vidas.render("INICIALES", True, BLANCO)
            puntuaciones = self.fuenteTemporizador.render("PUNTUACIONES", True, BLANCO)
        
            y = 10
            self.pantalla_principal.blit(iniciales,(10,y))
            self.pantalla_principal.blit(puntuaciones, (ANCHO // 2, y))

            for i,p in mejores3:
                y += 30
                iniciales = self.fuente_vidas.render(i, True, BLANCO)
                puntuaciones = self.fuenteTemporizador.render(str(p), True, BLANCO)
            
                self.pantalla_principal.blit(iniciales,(10,y))
                self.pantalla_principal.blit(puntuaciones, (ANCHO // 2, y))
            

            pg.display.flip()


            

        

#--Creo función para añadir obstaculos para cada Nivel--  

    def add_obstaculos(self, n_obstaculos):
         
        for i in range(n_obstaculos):
            obstaculo=Obstaculo(VELOCIDAD_NIVEL[self.nivel]) #creo un objeto obstaculo
            self.grupo_obstaculos.add(obstaculo) #para comprobar colisiones
            self.all_sprites.add(obstaculo) #para actualizar todos los sprites a la vez

#----Función para cambiar de nivel en función del tiempo transcurrido---
    def check_nivel(self):
        nivel_anterior=self.nivel
        #el temporizador es el tiempo desde que he iniciado la partida
        if self.temporizador> TIEMPO_N1:
            self.nivel=2
        elif self.temporizador>TIEMPO_N2:
            self.nivel=3
        
        if nivel_anterior != self.nivel:
            for obstaculo in self.grupo_obstaculos:
                obstaculo.cambia_velocidad(VELOCIDAD_NIVEL[self.nivel])
            self.add_obstaculos(2)

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
        
        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_instrucciones= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        

    def bucle_ppal(self):
        pg.display.set_caption("Instrucciones")

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
        

        self.imagenFondo= FONDO #pg.image.load("")
        self.fuente_puntuaciones= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
       


    def bucle_ppal(self):
        pg.display.set_caption("Puntuaciones")

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
        

        self.imagenFondo= FONDO #pg.image.load("")
        #self.imagenFondo=pg.transform.scale(self.imagenFondo,(ANCHO,ALTO))
        self.fuente_win= pg.font.Font("the_quest/fuentes/fast99.ttf",20)

       

        

    def bucle_ppal(self):
        pg.display.set_caption("WIN")
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
        
        self.imagenFondo= FONDO_GAME_OVER #pg.image.load("")
        self.imagenFondo=pg.transform.scale(self.imagenFondo,(ANCHO,ALTO))
        self.fuente_game= pg.font.Font("the_quest/fuentes/fast99.ttf",20)
        
    #def draw(self, pantalla):


    def bucle_ppal(self):
        pg.display.set_caption("GAME OVER")

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
            game=self.fuente_game.render("Pulsa Escape para volver al inicio", True, BLANCO)
            
            self.pantalla_principal.blit(game, (100, 400))
            
            
            pg.display.flip()

