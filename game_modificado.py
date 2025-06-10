import sys
import os
# Unir todos los archivos en 1 ejecutable
def recurso(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return ruta_relativa

#!/usr/bin/env python3
import pygame
import sys
import constantes
import sonidos
import Enemigos
from Powerups import PowerUp
from explosiones import Explosion
from personajes import Personaje
from weapons import Weapon
from bullets import Disparo
import csv
import random
import math
pygame.init()

screen = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
scroll_x = 0

disparos = pygame.sprite.Group()
screen.fill((0, 0, 0))
# Cargar imagenes de los botones
icono = pygame.image.load(recurso("Recursos//Sprites//Inicio//cursor_de_personaje//cursor_de_personaje2.png"))
icono = pygame.transform.scale(icono, (50, 50))
ESCALA_GLOBAL = constantes.ALTO / 245
# Cargar imagenes
creditos_img = pygame.image.load(recurso("Recursos/Sprites/interfaz/creditos/creditos.png")).convert_alpha()
escala_creditos_image = constantes.ALTO / 794
nuevo_ancho_escala_creditos_image = int(1123 * escala_creditos_image)
creditos_img = pygame.transform.scale(creditos_img, (constantes.ANCHO, constantes.ALTO))

start_img = pygame.image.load(recurso("Recursos//Sprites//Inicio//pantalla_inicial//pantalla_inicial2.png")).convert()
escala_start_image = constantes.ALTO / 794
nuevo_ancho_start_image = int(1123 * escala_start_image)
start_img = pygame.transform.scale(start_img, (constantes.ANCHO, constantes.ALTO))

# Extrae el tile a partir del ID del csv stage1
def obtener_tile(tileset, tile_id, tile_ancho, tile_alto, columnas_tileset):
    fila = tile_id // columnas_tileset
    columna = tile_id % columnas_tileset
    rect = pygame.Rect(columna * tile_ancho, fila * tile_alto, tile_ancho, tile_alto)
    return tileset.subsurface(rect)
# Carga la matriz del csv y lo mete en mapa = []
def cargar_mapa_csv(ruta_csv):
    
    mapa = []
    with open(ruta_csv, newline='') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            mapa.append(list(map(int, fila)))
    return mapa
# Recorre la matriz mapa, para cada ID vacio o que no sea cero se dibuja en screen
def dibujar_mapa(screen, mapa, tileset, tile_ancho, tile_alto, columnas_tileset):
   
    for y, fila in enumerate(mapa):
        for x, tile_id in enumerate(fila):
            if tile_id == 0:  # Salta los espacios vacíos
                continue
            # Si en el CSV los IDs comienzan en 1, restamos 1 para indexar el tileset.
            tile_img = obtener_tile(tileset, tile_id - 1, tile_ancho, tile_alto, columnas_tileset)
            screen.blit(tile_img, (x * tile_ancho, y * tile_alto))

ESCALA = 2
TILE_ANCHO = 32
TILE_ALTO = 32
TILES_COLISIONABLES = [325, 648]
# En base a la matriz mapa genera las colisiones y solo 325 y 648 son colisionables, todos los demas tiles te dejan caer
def crear_rectangulos_colision(mapa, escala):
    rects_colision = []
    for y, fila in enumerate(mapa):
        for x, tile_id in enumerate(fila):
            if tile_id in TILES_COLISIONABLES:
                rect = pygame.Rect( x * TILE_ANCHO * escala, y * TILE_ALTO * escala, TILE_ANCHO * escala, TILE_ALTO * escala)
                rects_colision.append(rect)
    return rects_colision
class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        
start_Button = Button(0, 0, start_img)

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size=(w * scale, h * scale))
    return nueva_imagen
def dibujar_texto(texto, fuente, color, x, y, escala=1):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect()
    rect_texto.topleft = (x, y)
    screen.blit(superficie_texto, rect_texto)

# Cargar FONDOS
pantalla_de_inicio = pygame.image.load(recurso("Recursos//Sprites//Inicio//pantalla_inicial//pantalla_inicial.png")).convert()
fondo = pygame.image.load(recurso("Recursos//Sprites//Stage_1//NES - Contra - Stage 1.png")).convert()
# Ancho real más grande que ANCHO de la ventana siempre
escala = constantes.ALTO / 245
nuevo_ancho = int(3456 * escala)
fondo = pygame.transform.scale(fondo, (nuevo_ancho, constantes.ALTO))
pantalla_de_inicio = pygame.transform.scale(pantalla_de_inicio, (nuevo_ancho, constantes.ALTO))

pygame.mixer.init()

def inicio_sonido():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//pantalla_de_inicio//retro-synth-loop-128-41048.mp3")) 
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)
    
def cursor():
    sonido_cursor = pygame.mixer.Sound(recurso("Recursos//Sonidos//pantalla_de_inicio//1or2players//arcade-ui-18-229517.mp3"))
    sonido_cursor.set_volume(0.5)
    sonido_cursor.play()
    
def tema_nvl():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//tema_primer_stage//game-over-groove-306764.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
def explocion():
    sonido_explosion = pygame.mixer.Sound(recurso("Recursos//Sonidos//death_personajes//8-bit-explosion-95847.mp3"))
    sonido_explosion.set_volume(0.5)
    sonido_explosion.play()
    
def creditos():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//Victoria//brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3"))
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)
    
def balas():
    sonido_balas = pygame.mixer.Sound(recurso("Recursos//Sonidos//shoot//shoot-6-81136.mp3"))
    sonido_balas.set_volume(0.5)
    sonido_balas.play()
def shootledaunenemigo():
    
    sonido_recibir_disparo = pygame.mixer.Sound(recurso("Recursos//Sonidos//Shootledaaunenemigo//391660__jeckkech__projectile.wav"))
    sonido_recibir_disparo.set_volume(0.5)
    sonido_recibir_disparo.play()
def power_up_sonido():
    
    sonido_recibir_disparo = pygame.mixer.Sound(recurso("Recursos//Sonidos//power_up//retro-video-game-coin-pickup-38299.mp3"))
    sonido_recibir_disparo.set_volume(0.5)
    sonido_recibir_disparo.play()
def explosion_enemigo():
    
    explosion_enemigo_bala = pygame.mixer.Sound(recurso("Recursos//Sonidos//death_personajes/retro-game-sfx-explosion-104422.mp3"))
    explosion_enemigo_bala.set_volume(0.5)
    explosion_enemigo_bala.play()
def game_over_sonido():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//game_over//videogame-death-sound-43894.mp3"))
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(1)

boss_channel = None

def boss_sonido():
    global boss_channel
    sonido_boss = pygame.mixer.Sound(recurso("Recursos//Sonidos//bossfinal//boom-sfx-318827.mp3"))
    sonido_boss.set_volume(0.5)
    
    boss_channel = sonido_boss.play(-1)

def detener_boss_sonido():
    global boss_channel
    if boss_channel is not None:
        boss_channel.stop()
        boss_channel = None  
def detener_tema_nvl():
    pygame.mixer.music.stop()




sprites_disparo = {
    "bala_1": escalar_img(pygame.image.load(recurso("Recursos/Sprites/Disparos/disparo_basico_S.png")).convert_alpha(), 1.5),
    "bala_2": escalar_img(pygame.image.load(recurso("Recursos/Sprites/Disparos/disparo_basico_S.png")).convert_alpha(), 4),
    "bala_3": escalar_img(pygame.image.load(recurso("Recursos/Sprites/Disparos/disparo_basico_S.png")).convert_alpha(), 1.5)
}
imagen_disparo_actual = sprites_disparo["bala_1"] 
# Todas las animaciones
    # personaje
animacion_nada = []
for i in range(1):
    imagen_quieto = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//mov_45_derecha_0.png")).convert_alpha()
    imagen_quieto = escalar_img(imagen_quieto, constantes.SCALA_PERSONAJE)
    animacion_nada.append(imagen_quieto)

nada = Weapon(animacion_nada)     

animaciones_sin_apuntar = []
for i in range(5):
    img = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_sin_apuntar_bill//mov_{i}_sin_apuntar.png"))
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones_sin_apuntar.append(img)
player_image = pygame.image.load(recurso("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_sin_apuntar_bill//mov_0_sin_apuntar.png"))
player_image = escalar_img(player_image, constantes.SCALA_PERSONAJE)

    

    # Armado
        # Derecha 45 grados
animaciones_apuntando_derecha = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//mov_45_derecha_{i}.png")).convert_alpha()
    imagen = escalar_img(imagen, constantes.SCALA_PERSONAJE)
    animaciones_apuntando_derecha.append(imagen)

apuntar_derecha = Weapon(animaciones_apuntando_derecha)  

        # arriba sin ciclo
animaciones_apuntando_arriba = []
for i in range(1):
    imagen = pygame.image.load(recurso("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_90//mov_apuntando_90_0.png")).convert_alpha()
    animaciones_apuntando_arriba.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_arriba = Weapon(animaciones_apuntando_arriba)
        # derecha recto
animaciones_apuntando_derecha_bien_derecha = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_dereha//mov_apuntando_derecha_{i}.png")).convert_alpha()
    animaciones_apuntando_derecha_bien_derecha.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_derecha_recto = Weapon(animaciones_apuntando_derecha_bien_derecha)

        # apuntar 315 grados
animaciones_apuntando_derecha_abajo = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_315_derecha//mov_315_derecha_{i}.png")).convert_alpha()
    animaciones_apuntando_derecha_abajo.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_derecha_abajo = Weapon(animaciones_apuntando_derecha_abajo)

        # agachado
animaciones_agachado = []
for i in range(1):
    imagen = pygame.image.load(recurso("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_agachado//mov_agachado_0.png")).convert_alpha()
    animaciones_agachado.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_agachado = Weapon(animaciones_agachado)   

        #saltando
        
animaciones_saltando = []
for i in range(1):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//salto_bill//salto_{i}.png")).convert_alpha()
    animaciones_saltando.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

saltar = Weapon(animaciones_saltando)           
        
        
# Animaciones para el enemigo 
animaciones_enemigo = []
for i in range(5):
    img = pygame.image.load(recurso(f"Recursos//Sprites//Enemigos//enemigos_que_si_se_mueven//enemigo_{i}.png")).convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones_enemigo.append(img) 
    
animacion_explosion = []
for i in range(5):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//explosiones//explosion_{i}.png")).convert_alpha()
    imagen_escalada = escalar_img(imagen, constantes.SCALA_PERSONAJE) 
    animacion_explosion.append(imagen_escalada)
    
    


powerup_resources = {
    "R": escalar_img(pygame.image.load(recurso("Recursos/Sprites/powerups/R.png")).convert_alpha(), 1.5),
    "S": escalar_img(pygame.image.load(recurso("Recursos/Sprites/powerups/S.png")).convert_alpha(), 1.5),
}


animaciones_apuntando_izquierda = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_dereha//izquierda//mov_apuntando_izquierda_{i}.png")).convert_alpha()
    animaciones_apuntando_izquierda.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_izquierda = Weapon(animaciones_apuntando_izquierda)

animaciones_apuntando_izquierda_izquierda = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//izquierda//mov_45_izquierda_{i}.png")).convert_alpha()
    animaciones_apuntando_izquierda_izquierda.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_izquierda_izquierda = Weapon(animaciones_apuntando_izquierda_izquierda)

animaciones_apuntando_izquierda_abajo = []
for i in range(2):
    imagen = pygame.image.load(recurso(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_315_derecha//izquierda//mov_315_izquierda_{i}.png")).convert_alpha()
    animaciones_apuntando_izquierda_abajo.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_abajo_izquierda = Weapon(animaciones_apuntando_izquierda_abajo)




# fuentes
font_inicio = pygame.font.Font(recurso("Recursos//letra//PressStart2P-Regular.ttf"), 25)
font_titulo = pygame.font.Font(recurso("Recursos//letra//PressStart2P-Regular.ttf"), 25)

controles = pygame.image.load(recurso("Recursos//letra//controles.jpg"))



#Botones 
boton_jugar1p = pygame.Rect(170, 570, 450, 50)
boton_salir = pygame.Rect(170,650, 200, 50)

boton_controles = pygame.Rect(1000, 650, 200, 50)

boton_regresar = pygame.Rect(1000,650, 250, 50)

boton_siguiente = pygame.Rect(1000, 590, 250, 50)


# Texto
texto_boton_salir = font_inicio.render("Salir", True, constantes.BLANCO)

texto_regresar = font_inicio.render("Regresar", True, constantes.BLANCO)

texto_siguiente = font_inicio.render("Siguiente", True, constantes.BLANCO)

texto_boton_controles = font_inicio.render("Controles", True, constantes.BLANCO)



def pantalla_inicio():
    screen.fill((30, 30, 30))
    start_Button.draw()
    
    pygame.draw.rect(screen,constantes.COLOR_BG, boton_salir)
    pygame.draw.rect(screen,constantes.COLOR_BG, boton_controles)
    # texto botones
    
    screen.blit(texto_boton_salir, (boton_salir.x + 30, boton_salir.y + 10))
    screen.blit(texto_boton_controles,(boton_controles.x + 30, boton_controles.y + 10))


# Efecto entre pantalla y pantalla
def fade(screen, color=(0, 0, 0), speed=10):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)


run = True
def pantalla_controles():
    run = True
    clock = pygame.time.Clock()

    # Centrar la imagen
    controles_rect = controles.get_rect(center=(constantes.ANCHO // 2, constantes.ALTO // 3))

    while run:
        screen.fill((30, 30, 30))

        # Fondo: imagen de controles
        screen.blit(controles, controles_rect)

        # Encima: texto y botón "Regresar"
        texto = font_inicio.render("PANTALLA DE CONTROLES", True, (255, 255, 255))
        screen.blit(texto, (constantes.ANCHO // 2 - texto.get_width() // 2, 30))

        # Dibuja botón
        pygame.draw.rect(screen, constantes.COLOR_BG, boton_regresar)
        screen.blit(texto_regresar, (boton_regresar.x + 30, boton_regresar.y + 10))

        # Icono si el mouse está encima
        mouse_pos = pygame.mouse.get_pos()
        if boton_regresar.collidepoint(mouse_pos):
            screen.blit(icono, (boton_regresar.left - icono.get_width() - 10, boton_regresar.centery - icono.get_height() // 2))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                sonidos.cursor()
                if boton_regresar.collidepoint(event.pos):
                    fade(screen)
                    inicio()
                    return

        disparos.update()
        disparos.draw(screen)

        pygame.display.update()
        clock.tick(60)




 
    
def pantalla_victoria():
    # Detenemos el sonido del boss y activamos la música de créditos
    detener_boss_sonido()
    creditos()
    creditos_img = pygame.image.load(recurso("Recursos/Sprites/interfaz/creditos/creditos.png")).convert_alpha()
    escala_creditos_image = constantes.ALTO / 794
    nuevo_ancho_escala_creditos_image = int(1123 * escala_creditos_image)
    creditos_img = pygame.transform.scale(creditos_img, (1800 , 1700))
    # Cargamos las fuentes y preparamos los mensajes
    font_inicio = pygame.font.Font(recurso("Recursos//letra//PressStart2P-Regular.ttf"), 25)
    mensaje = font_inicio.render("¡Ganaste!", True, (255, 255, 255))
    
    font_pequeno = pygame.font.Font(recurso("Recursos//letra//PressStart2P-Regular.ttf"), 40)
    reiniciar_texto = font_pequeno.render("Presiona R para volver al inicio", True, (200, 200, 200))
    
    clock = pygame.time.Clock()
    esperando = True

    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    fade(screen)
                    inicio()  
                    esperando = False

        # Rellenamos la pantalla y dibujamos la imagen de créditos junto con los textos
        screen.fill((0, 0, 0))
        
        
        screen.blit(creditos_img, (-scroll_x, 0))
        screen.blit(mensaje, (constantes.ANCHO // 2 - mensaje.get_width() // 2,constantes.ALTO // 2 - mensaje.get_height() // 2 - 30))
        screen.blit(reiniciar_texto, (constantes.ANCHO // 2 - reiniciar_texto.get_width() // 2,constantes.ALTO // 2 + 40))

        pygame.display.update()
        clock.tick(60)
        

def pantalla_game_over(screen):
    
    game_over_sonido()
    font = pygame.font.SysFont(None, 72)
    texto_game_over = font.render("GAME OVER", True, (255, 0, 0))
    texto_reiniciar = font.render("Presiona R para reiniciar", True, (255, 255, 255))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(texto_game_over, (screen.get_width()//2 - texto_game_over.get_width()//2, 200))
        screen.blit(texto_reiniciar, (screen.get_width()//2 - texto_reiniciar.get_width()//2, 300))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tema_nvl()
                    juego()      
     


# Clase Boss, la pusimos aqui por que estaba generando muchos errores en otro archivo por que usa las balas y la explosion
class Boss(pygame.sprite.Sprite):
    def __init__(self, position, health, sprite_image, animacion_explosion, bullet_image, projectiles_group):
        super().__init__()
        self.image = sprite_image
        self.rect = self.image.get_rect(center=position)
        self.health = self.max_health = health

        self.shoot_cooldown = 1000  # ms
        self.last_shot_time = pygame.time.get_ticks()
        self.bullet_image = bullet_image
        self.projectiles_group = projectiles_group

        self.velocity = 4
        self.direction = 1
        self.limite_izquierdo = position[0] - 0
        self.limite_derecho = position[0] +0

        self.exploding = False
        self.explosion_frames = animacion_explosion
        self.explosion_index = 0
        self.explosion_update_time = 0
        self.explosion_cooldown = 100  # ms

    def update(self, player, clase_disparo):
        if self.exploding:
            explosion_enemigo()
            self.actualizar_explosion()
            return

        
        self.disparar_si_corresponde(player, clase_disparo)

        if self.rect.colliderect(player.shape):
            player.alive = False

    def mover(self):
        self.rect.x += self.velocity * self.direction
        
        if self.rect.left < self.limite_izquierdo or self.rect.right > self.limite_derecho:
            self.direction *= -1
           
    def disparar_si_corresponde(self, player, clase_disparo):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.last_shot_time >= self.shoot_cooldown:
           
            self.shoot(player, clase_disparo)
            self.last_shot_time = tiempo_actual

    def shoot(self, player, clase_disparo):
        boss_center = self.rect.center
        player_center = player.shape.center
        dx = player_center[0] - boss_center[0]
        dy = player_center[1] - boss_center[1]
        angle = math.atan2(dy, dx)

        velocidad = 5
        vel_x = velocidad * math.cos(angle)
        vel_y = velocidad * math.sin(angle)

      

        nueva_bala = clase_disparo(boss_center[0], boss_center[1], vel_x, vel_y, self.bullet_image)
        self.projectiles_group.add(nueva_bala)

    def actualizar_explosion(self):
        now = pygame.time.get_ticks()
        if now - self.explosion_update_time > self.explosion_cooldown:
            self.explosion_index += 1
            self.explosion_update_time = now
            if self.explosion_index < len(self.explosion_frames):
                # Escalamos la imagen para que la explosión se vea más grande 
                frame_original = self.explosion_frames[self.explosion_index]
                ancho = frame_original.get_width() * 10 
                alto = frame_original.get_height() * 10
                self.image = pygame.transform.scale(frame_original, (ancho, alto))
            else:
                # Si no se ha registrado aún el tiempo de término de la explosión se debe registrar.
                if not hasattr(self, "explosion_finish_time"):
                    self.explosion_finish_time = now
                # Esperamos 2000 ms adicionales 
                elif now - self.explosion_finish_time > 500:
                    self.kill()   
                    fade(screen)
                    pantalla_victoria()  

    def draw(self, surface, scroll_x=0):
        surface.blit(self.image, (self.rect.x - scroll_x, self.rect.y))
        self.draw_health_bar(surface, scroll_x)

    def draw_health_bar(self, surface, scroll_x=0):
        bar_width = self.rect.width
        bar_height = 10
        x = self.rect.x - scroll_x
        y = self.rect.y - 15

        health_ratio = max(0, self.health / self.max_health)
        fill_width = int(bar_width * health_ratio)

        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, fill_width, bar_height))

    def recibir_daño(self, cantidad):
        self.health -= cantidad
        if self.health <= 0:
            self.exploding = True
            self.explosion_index = 0
            self.explosion_update_time = pygame.time.get_ticks()  


class DisparoEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        global scroll_x  
        # Calculamos la posición de la bala en la pantalla
        pantalla_x = self.rect.x - scroll_x  
        # Verificamos si la bala está fuera de la pantalla 
        if (pantalla_x + self.rect.width < 0 or pantalla_x > 1280 or
            self.rect.bottom < 0 or self.rect.top > 720):
            self.kill()
     
def juego():
    
   # Cargar y escalar la imagen del disparo enemigo
    imagen_bala_enemiga = pygame.image.load(recurso("Recursos/Sprites/Disparos/disparo_basico_F.png")).convert_alpha()
    imagen_bala_enemiga = pygame.transform.scale(imagen_bala_enemiga, (20, 10))
    
    # Cargar y escalar sprite del boss usando función propia (escala_img)
    boss_sprite = pygame.image.load(recurso("Recursos/Sprites/Defensa_boss stage_1/NES - Contra - Defense Wall.png")).convert_alpha()
    boss_sprite = escalar_img(boss_sprite, 3)
    balas_boss = pygame.sprite.Group()
    # Definir la zona en la que se activa el boss (coordenadas según tu nivel)
    zona_boss = pygame.Rect(9300, 0, 400, constantes.ALTO)
    # Crear al boss
    boss = Boss(
        position=(10000, 400),health=10,sprite_image=boss_sprite,animacion_explosion=animacion_explosion,bullet_image=imagen_bala_enemiga,projectiles_group=balas_boss)
        
    
    def cambiar_tipo_disparo(jugador, nuevo_tipo):
        # Dicciopnario global de disparos del inicio
        global sprites_disparo  
        if nuevo_tipo in sprites_disparo:
            # Modificamos el atributo del jugador
            jugador.tipo_disparo = nuevo_tipo  
          
        

    weapons_dict = {
        "nada": nada,
        "arriba": apuntar_arriba,
        "derecha": apuntar_derecha,
        "derecharecto": apuntar_derecha_recto,
        "derechaabajo": apuntar_derecha_abajo,
        "abajo": apuntar_agachado,
        "saltar": saltar,
        "izquierda": apuntar_izquierda,
        "izquierda_arriba": apuntar_izquierda_izquierda,
        "izquierda_abajo": apuntar_abajo_izquierda
        
    }

    jugador = Personaje(100, 225, animaciones_sin_apuntar, weapons_dict, animaciones_saltando)
    jugador.en_suelo = True
    jugador.COYOTE_TIME_MAX = 150
    jugador.coyote_timer = jugador.COYOTE_TIME_MAX

    enemigo1 = Enemigos.Enemigo(100, 225, animaciones_enemigo)
    
    pygame.font.init()
    hud_font = pygame.font.SysFont("Arial", 24)
    TILE_ANCHO = 32
    TILE_ALTO = 32
    COLUMNAS_TILESET = 108
    TILES_COLISIONABLES = [325, 648]
    
    
    
    # Cargamos primero el csv de las colisiones y despues encima el png del mapa
    mapa = cargar_mapa_csv(recurso("Recursos/Sprites/Stage_1/stage1.csv"))
    tileset = pygame.image.load(recurso("Recursos/Sprites/Stage_1/NES - Contra - Stage 1.png")).convert_alpha()

    def crear_rectangulos_colision(mapa, tile_ancho, tile_alto):
        rects = []
        for y, fila in enumerate(mapa):
            for x, tile_id in enumerate(fila):
                if tile_id in TILES_COLISIONABLES:
                    rect = pygame.Rect(x * tile_ancho, y * tile_alto, tile_ancho, tile_alto)
                    rects.append(rect)
        return rects
 
    
     
    altura_enemigo = 32  
   
    rects_colision = crear_rectangulos_colision(mapa, TILE_ANCHO, TILE_ALTO)
    imagen_bala = sprites_disparo["bala_1"]
    scroll_x = 0
    gravedad = 1
    clock = pygame.time.Clock()
    run = True
    mover_derecha = False
    mover_izquierda = False
    # Zona de victoria definida manualmente 
    zona_victoria = pygame.Rect(9750, 400, 64, 64)
    disparos = pygame.sprite.Group()
    muertos = 0
    explosiones = [] 
    jugador.vida = 5
    boss_sound_played = False
    animaciones_power_up = [powerup_resources["R"], powerup_resources["S"]]
    
    # Definir la lista de power‑ups
    power_ups = [] 
    
    def draw_health_bar(surface, world_x, world_y, width, height, current_health, max_health, scroll_x=0):
        
        # Dibuja una barra de vida en función de la posición en el mundo (world_x, world_y).
        # Se ajusta automáticamente restando scroll_x para obtener la posición en pantalla.
        
        # Convertir las coordenadas del mundo a coordenadas en pantalla
        x_on_screen = world_x - scroll_x
        y_on_screen = world_y
    
        # Fondo de la barra 
        background_rect = pygame.Rect(x_on_screen, y_on_screen, width, height)
        pygame.draw.rect(surface, (255, 0, 0), background_rect)
    
        # Ancho de la barra verde (vida actual)
        health_width = int(width * (current_health / max_health))
        health_rect = pygame.Rect(x_on_screen, y_on_screen, health_width, height)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)
    
    def generar_un_enemigo(rects_colision, altura_enemigo, animaciones_enemigo, jugador, enemigos_existentes):
        # Define qué tan cerca debe estar el jugador para generar enemigos
        distancia_maxima = 2000
    
        
        posibles_posiciones = [rect for rect in rects_colision if abs(jugador.world_x - rect.x) < distancia_maxima]
    
        if posibles_posiciones:  
            rect_seleccionado = random.choice(posibles_posiciones)  # Elegir una posicion al azar
    
            # Verificar que no haya un bloque encima para evitar spawns dentro de paredes
            hay_bloque_encima = any(
                otro.left == rect_seleccionado.left and otro.top == rect_seleccionado.top - rect_seleccionado.height
                for otro in rects_colision
            )
    
            # Evitar duplicados basados en coordenada X
            if not hay_bloque_encima and not any(enemigo.rect.x == rect_seleccionado.x for enemigo in enemigos_existentes):
                x = rect_seleccionado.x
                y = rect_seleccionado.y - altura_enemigo
                enemigo = Enemigos.Enemigo(x, y, animaciones_enemigo)
                enemigos_existentes.add(enemigo)
    
        return enemigos_existentes
    enemigos = pygame.sprite.Group()
    ultimo_spawn = pygame.time.get_ticks()
    while run:
        
        
        dt = clock.tick(60)
        
        tiempo_actual = pygame.time.get_ticks()

        for enemigo in list(enemigos):
            if enemigo.rect.right < scroll_x - 50:  
                enemigos.remove(enemigo)
        
        # Generación de 1 enemigo cada 10 segundos
        if tiempo_actual - ultimo_spawn > 1000:  # 10 segundos
            prev_count = len(enemigos)
            enemigos = generar_un_enemigo(rects_colision, altura_enemigo, animaciones_enemigo, jugador, enemigos)
            if len(enemigos) > prev_count:  # Solo reiniciar el temporizador si se creó un enemigo
                ultimo_spawn = tiempo_actual
 
        
     
        screen.fill((0, 0, 0))
        dibujar_mapa(screen, mapa, tileset, TILE_ANCHO, TILE_ALTO, COLUMNAS_TILESET)
        screen.blit(fondo, (-scroll_x, 0))
        

        pos_pantalla_x = jugador.world_x - scroll_x
        pos_pantalla_y = jugador.world_y
        jugador.shape.topleft = (pos_pantalla_x, pos_pantalla_y)
        
        zona_dibujo = zona_victoria.copy()
        zona_dibujo.x -= scroll_x
        
        jugador_mundo_rect = jugador.shape.copy()
        jugador_mundo_rect.x = jugador.world_x
        jugador_mundo_rect.y = jugador.world_y
        
        if not jugador.alive:
            pantalla_game_over(screen)
            # Reiniciar el juego al regresar
            fade(screen)
            juego()  
            return
        if jugador.shape.top > constantes.ALTO:
            
            jugador.alive = False
        
        if jugador.reloading:
            ammo_text = "Recargando..."
            color = (255, 0, 0)  # Rojo 
        else:
            ammo_text = f"Munición: {jugador.ammo_actual}/{jugador.ammo_max}"
            color = (255, 255, 255)  # Blanco
        
        
        
        boss.update(jugador, DisparoEnemigo)
        boss.draw(screen, scroll_x)
        
        balas_boss.update()
        for bala in balas_boss:
            screen.blit(bala.image, (bala.rect.x - scroll_x, bala.rect.y))
        
        # Colisiones balas del boss con jugador
        for bala in balas_boss:
            if bala.rect.colliderect(jugador.shape):
                bala.kill()
        hud_surface = font_inicio.render(ammo_text, True, color)
        screen.blit(hud_surface, (20, 20))
        
        
        teclas = pygame.key.get_pressed()
        delta_x = 0
        if  teclas[pygame.K_RIGHT]:  
            delta_x = constantes.VELOCIDAD
        elif teclas[pygame.K_LEFT]:  
             delta_x = -constantes.VELOCIDAD

        # Actualiza el coyote timer
        if jugador.en_suelo:
            jugador.coyote_timer = jugador.COYOTE_TIME_MAX
        else:
            jugador.coyote_timer -= dt
            jugador.coyote_timer = max(0, jugador.coyote_timer)

        puede_saltar = (jugador.en_suelo or jugador.coyote_timer > 0) and jugador.vel_y >= 0
        if teclas[pygame.K_SPACE] and puede_saltar:
            jugador.vel_y = -20
            jugador.en_suelo = False
            jugador.saltando = True
            jugador.coyote_timer = 0

        jugador.vel_y += gravedad
        jugador.vel_y = min(jugador.vel_y, 10)
        delta_y = jugador.vel_y

        jugador.movimiento(delta_x, delta_y, rects_colision)

        # Define una zona para activar la fase del boss
        zona_boss = pygame.Rect(9300, 0, 400, constantes.ALTO)
        
        # Determina si estamos en la fase boss
        boss_activo = jugador.world_x >= zona_boss.x
        
        
        
        if boss_activo:
            # Si el sonido del boss aún no se ha reproducido, se reproduce y se marca la bandera para poder quitarlo despues por que generaba errores si solo llamabas a la funcion
            if not boss_sound_played:
                detener_tema_nvl()
                boss_sonido()
                boss_sound_played = True
            # Centramos la cámara en el boss
            nuevo_scroll = boss.rect.centerx - (constantes.ANCHO // 2)
            scroll_x += (nuevo_scroll - scroll_x) * 0.1  # factor de suavizado
        else:
            #
            boss_sound_played = False
            if jugador.world_x - scroll_x > constantes.ANCHO // 2:
                scroll_x += delta_x
            elif jugador.world_x - scroll_x < constantes.ANCHO // 2:
                scroll_x += delta_x
            else:
                jugador.world_x += delta_x
        
        # Actualiza la posición en pantalla del jugador
        jugador.shape.x = jugador.world_x - scroll_x

        if jugador.shape.left < 50:
            jugador.shape.left = 50
            jugador.world_x = jugador.shape.x + scroll_x
        if jugador.shape.right > constantes.ANCHO - 10:
            jugador.shape.right = constantes.ANCHO - 10
            jugador.world_x = jugador.shape.x + scroll_x
        if jugador.shape.bottom > constantes.ALTO:
            jugador.alive = False

      

        for rect in rects_colision:
            rect_debug = rect.copy()
            rect_debug.x -= scroll_x
            

        direccion_apuntado = None
        if teclas[pygame.K_UP] and teclas[pygame.K_RIGHT]:
            direccion_apuntado = "derecha"
        elif teclas[pygame.K_UP] and teclas[pygame.K_LEFT]:
            direccion_apuntado = "izquierda_arriba"
        elif teclas[pygame.K_DOWN] and teclas[pygame.K_LEFT]:
            direccion_apuntado = "izquierda_abajo"
        elif teclas[pygame.K_UP]:
            direccion_apuntado = "arriba"
        elif teclas[pygame.K_RIGHT]:
            direccion_apuntado = "derecharecto"
        elif teclas[pygame.K_LEFT]:
            direccion_apuntado = "izquierda"
        elif teclas[pygame.K_DOWN]:
            # Mientras esté agachado, forzamos la dirección hacia la derecha
            direccion_apuntado = "abajo"
            jugador.flip = False  # Mira a la derecha
        elif teclas[pygame.K_SPACE]:
            direccion_apuntado = "saltar"
        else:
            direccion_apuntado = None

        if not jugador.saltando:
            if direccion_apuntado:
                jugador.set_apuntado(True, direccion_apuntado)
            else:
                jugador.set_apuntado(False)
                
                
        explosion_actual = None
        jugador.update()
        enemigos.update(rects_colision) 
        for enemigo in enemigos:
            screen.blit(enemigo.image, (enemigo.rect.x - scroll_x, enemigo.rect.y))
            draw_health_bar(screen, enemigo.rect.x, enemigo.rect.y - 10, 40, 5, enemigo.vida, 3, scroll_x)
        for bala in list(disparos):
            # Colision con el scroll
            if bala.rect.colliderect(boss.rect):
                boss.recibir_daño(bala.daño)  
                disparos.remove(bala)
               
        
        
            # Colisión bala-enemigo
        for bala in list(disparos):  
            for enemigo in list(enemigos):
                if bala.rect.colliderect(enemigo.rect) and enemigo.alive:
                    enemigo.vida -= bala.daño
                    disparos.remove(bala)
                    shootledaunenemigo()
                    if enemigo.vida <= 0:
                       
                      
                        enemigo.alive = False
                        
                        enemigos.remove(enemigo)
                        explosion_enemigo()
                        muertos += 1
                        if random.random() < 0.10:
                            power_up = PowerUp(enemigo.rect.x, enemigo.rect.y, animaciones_power_up)
                            power_ups.append(power_up)
                    break  
    
        for enemigo in list(enemigos):
            
            enemy_screen_rect = enemigo.rect.copy()
            enemy_screen_rect.x -= scroll_x
           
            if jugador.shape.colliderect(enemy_screen_rect) and enemigo.alive:
              
                jugador.vida -= 1
             
                explosiones.append(Explosion(enemy_screen_rect.centerx,enemy_screen_rect.centery,animacion_explosion))
                enemigo.alive = False
                explocion()
                enemigos.remove(enemigo)
                explosion_enemigo()
                if jugador.vida <= 0:
                    pantalla_game_over(screen)
                    juego()
                    fade(screen)
             
                break
      
        for explosion in list(explosiones):
            explosion.update()
            explosion.draw(screen)
            if not explosion.activa:  # Cuando la animación termina
                explosiones.remove(explosion)
        for powerup in list(power_ups):
            powerup.update(rects_colision)
            powerup.draw(screen, scroll_x)
        
            powerup_screen_rect = powerup.shape.copy()
            powerup_screen_rect.x -= scroll_x  # Ajustado por el scroll
            # Tocar el power up te cambia de disparo
            if jugador.shape.colliderect(powerup_screen_rect):
                power_up_sonido()
                cambiar_tipo_disparo(jugador, "bala_2") 
                power_ups.remove(powerup)
            
            
        
            
        jugador.draw(screen, scroll_x)
        draw_health_bar(screen, jugador.world_x, jugador.world_y - 30, 50, 6, jugador.vida, jugador.vida_maxima, scroll_x)
        disparos.update()
        

        for disparo in disparos:
            screen.blit(disparo.image, (disparo.rect.x - scroll_x, disparo.rect.y))
       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade(screen)
                    inicio()
                elif event.key == pygame.K_r:
                    fade(screen)
                    inicio()
                elif event.key == pygame.K_c and direccion_apuntado and not jugador.saltando:
                    if jugador.reloading:
                        
                        continue  # No se procesa el disparo
                    
        
                    # Obtiene el tiempo actual
                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_actual - jugador.last_shot_time < jugador.fire_rate:
                        
                        continue
        
                    jugador.last_shot_time = tiempo_actual
                    sonidos.balas()
                    teclas = pygame.key.get_pressed()
                    direccion = None
        
                    # Direccion
                    if teclas[pygame.K_UP] and teclas[pygame.K_RIGHT]:
                        direccion = "derecha"
                    elif teclas[pygame.K_UP] and teclas[pygame.K_LEFT]:
                        direccion = "izquierda_arriba"
                    elif teclas[pygame.K_UP]:
                        direccion = "arriba"
                    elif teclas[pygame.K_RIGHT]:
                        direccion = "derecharecto"
                    elif teclas[pygame.K_DOWN] and teclas[pygame.K_LEFT]:
                        direccion = "izquierda_abajo"
                    elif teclas[pygame.K_LEFT]:
                        direccion = "izquierda"
                    elif teclas[pygame.K_DOWN]:
                        direccion = "abajo"
                    else:
                        direccion = "derecharecto"  # Valor por defecto
        
                    mirar_izquierda = jugador.flip
        
                    # Cálculo de offsets o para qe entienda Jesus es la posicion de la bala dependiendo de hacia donde este apuntando
                    if direccion in ["derecha", "derecharecto", "derechaabajo"]:
                        offset_x = 40 if not mirar_izquierda else -10
                        offset_y = 10
                    elif direccion in ["izquierda", "izquierda_arriba", "izquierda_abajo"]:
                        offset_x = -10 if mirar_izquierda else 40
                        offset_y = 10
                    elif direccion == "arriba":
                        offset_x = 20
                        offset_y = -10
                    elif direccion == "abajo":
                        offset_x = 20
                        offset_y = 15
                    else:
                        offset_x = 20
                        offset_y = 10
        
                    # Calcula la posición del disparo usando coordenadas del mundo para que se mueva y no se quede estatica
                    bala_x = jugador.world_x + offset_x
                    bala_y = jugador.world_y + offset_y
                    
                    # Municion
                    cost = 2 if jugador.tipo_disparo == "bala_2" else 1
                    if jugador.ammo_actual >= cost:
                        nuevo_disparo = Disparo(
                            bala_x,
                            bala_y,
                            direccion,
                            sprites_disparo[jugador.tipo_disparo],
                            tipo=jugador.tipo_disparo,
                            mirar_izquierda=mirar_izquierda
                        )
                        disparos.add(nuevo_disparo)
                        jugador.ammo_actual -= cost
                        
                    else:
                        jugador.reloading = True
                        jugador.last_reload_time = pygame.time.get_ticks()
                        
            
                    jugador.set_apuntado(True, direccion)
        
                
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        mover_derecha = True
                    if event.key == pygame.K_a:
                        mover_izquierda = True
            
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        mover_derecha = False
                    if event.key == pygame.K_a:
                        mover_izquierda = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouse_pos = pygame.mouse.get_pos()
                    boton_regresar = pygame.Rect(50, 700, 250, 50)
                    if boton_regresar.collidepoint(mouse_pos):
                        
                        fade(screen)
                        inicio()
        
        pygame.display.update()
    
clock = pygame.time.Clock()
# Esto llama a todas las pantallas posibles
def inicio():
    sonido_reproducido = False
    run = True 
    estado = "inicio"
    mostrar_controles = False
    mostrar_inicio = True
    inicio_sonido()
    while run: 
        
        
        if mostrar_inicio == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_jugar1p.collidepoint(event.pos):
                        if boton_jugar1p.collidepoint(event.pos):
                            sonidos.cursor()
                            fade(screen)
                            tema_nvl()            
                            estado = "juego"
                    elif boton_salir.collidepoint(event.pos):
                        sonidos.cursor()
                        fade(screen)
                        run = False
                    elif boton_controles.collidepoint(event.pos):
                        sonidos.cursor()
                        estado = "controles"
                        fade(screen)
                    elif boton_siguiente.collidepoint(event.pos):
                        sonidos.cursor()
                        estado = "controles_apuntar"
                        fade(screen)
                     
                     
                     
             
                 
                 
            if estado == "inicio":
                pantalla_inicio()
                mouse_pos = pygame.mouse.get_pos()
                if boton_jugar1p.collidepoint(mouse_pos): 
                    screen.blit(icono, (boton_jugar1p.left - icono.get_width() - 10, boton_jugar1p.centery - icono.get_height() // 2))
                if boton_salir.collidepoint(mouse_pos): 
                    screen.blit(icono, (boton_salir.left - icono.get_width() - 10, boton_salir.centery - icono.get_height() // 2))
                if boton_controles.collidepoint(mouse_pos): 
                    screen.blit(icono, (boton_controles.left - icono.get_width() - 10, boton_controles.centery - icono.get_height() // 2))
                    
                
                pygame.display.update()
                clock.tick(60)
            if estado == "controles":
                
                pantalla_controles()
                
                
            
            if estado == "juego":
               
              
               juego()
                
            

        

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


inicio()
pygame.quit()
sys.exit()
