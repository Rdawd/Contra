#!/usr/bin/env python3
import pygame
import sys
import constantes
import Enemigos
from Powerups import PowerUp
from explosiones import Explosion
from personajes import Personaje
from weapons import Weapon
from bullets import Disparo
import csv



pygame.init()

screen = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
scroll_x = 0

disparos = pygame.sprite.Group()
screen.fill((0, 0, 0))
# Cargar imagenes de los botones
icono = pygame.image.load("Recursos//Sprites//Inicio//cursor_de_personaje//cursor_de_personaje2.png")
icono = pygame.transform.scale(icono, (50, 50))

# Tamaño tile
TILE_SIZE = 32

# Leer CSV y cargar matriz
world_data = []
with open(r"Recursos//Mapa_Prueba_Shi.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for fila in reader:
        world_data.append([int(columna) for columna in fila])

# Crear rects de colisión
rects_colision = []
for fila_idx, fila in enumerate(world_data):
    for col_idx, celda in enumerate(fila):
        if celda == 1:  # Solo las plataformas sólidas o atravesables que definas como 1
            x = col_idx * TILE_SIZE
            y = fila_idx * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            rects_colision.append((rect, celda))


start_img = pygame.image.load("Recursos//Sprites//Inicio//pantalla_inicial//pantalla_inicial2.png").convert()
escala_start_image = constantes.ALTO / 794
nuevo_ancho_start_image = int(1123 * escala_start_image)
start_img = pygame.transform.scale(start_img, (nuevo_ancho_start_image , constantes.ALTO))

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


pantalla_de_inicio = pygame.image.load("Recursos//Sprites//Inicio//pantalla_inicial//pantalla_inicial.png").convert()
fondo = pygame.image.load("Recursos//Sprites//Stage_1//NES - Contra - Stage 1.png").convert()
# anchoo real más grande que ANCHO de la ventana
escala = constantes.ALTO / 245
nuevo_ancho = int(3456 * escala)
fondo = pygame.transform.scale(fondo, (nuevo_ancho, constantes.ALTO))
pantalla_de_inicio = pygame.transform.scale(pantalla_de_inicio, (nuevo_ancho, constantes.ALTO))
pygame.mixer.init() 
inicio = pygame.mixer.music.load("Recursos//Sonidos//pantalla_de_inicio//retro-synth-loop-128-41048.mp3") 
inicio = pygame.mixer.music.set_volume(0.5)
inicio = pygame.mixer.music.set_volume(0.01)
inicio = pygame.mixer.music.play(-1)
  







sprites_disparo = {
    "bala_1": escalar_img(pygame.image.load("Recursos/Sprites/Disparos/disparo_basico_S.png").convert_alpha(), 1.5),
    # ""bala_2": escalar_img(pygame.image.load("Recursos/Sprites/Disparos/bala2.png").convert_alpha(), 1.0),
    # "laser": escalar_img(pygame.image.load("Recursos/Sprites/Disparos/laser.png").convert_alpha(), 0.5),
}
imagen_disparo_actual = sprites_disparo["bala_1"] 
# Todas las animaciones
    # personaje
animacion_nada = []
for i in range(1):
    imagen_quieto = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//mov_45_derecha_0.png").convert_alpha()
    imagen_quieto = escalar_img(imagen_quieto, constantes.SCALA_PERSONAJE)
    animacion_nada.append(imagen_quieto)

nada = Weapon(animacion_nada)     

animaciones_sin_apuntar = []
for i in range(5):
    img = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_sin_apuntar_bill//mov_{i}_sin_apuntar.png")
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones_sin_apuntar.append(img)
player_image = pygame.image.load("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_sin_apuntar_bill//mov_0_sin_apuntar.png")
player_image = escalar_img(player_image, constantes.SCALA_PERSONAJE)

    

    # Armado
        # Derecha 45 grados
animaciones_apuntando_derecha = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//mov_45_derecha_{i}.png").convert_alpha()
    imagen = escalar_img(imagen, constantes.SCALA_PERSONAJE)
    animaciones_apuntando_derecha.append(imagen)

apuntar_derecha = Weapon(animaciones_apuntando_derecha)  

        # arriba sin ciclo
animaciones_apuntando_arriba = []
for i in range(1):
    imagen = pygame.image.load("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_90//mov_apuntando_90_0.png").convert_alpha()
    animaciones_apuntando_arriba.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_arriba = Weapon(animaciones_apuntando_arriba)
        # derecha recto
animaciones_apuntando_derecha_bien_derecha = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_dereha//mov_apuntando_derecha_{i}.png").convert_alpha()
    animaciones_apuntando_derecha_bien_derecha.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_derecha_recto = Weapon(animaciones_apuntando_derecha_bien_derecha)

        # apuntar 315 grados
animaciones_apuntando_derecha_abajo = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_315_derecha//mov_315_derecha_{i}.png").convert_alpha()
    animaciones_apuntando_derecha_abajo.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_derecha_abajo = Weapon(animaciones_apuntando_derecha_abajo)

        # agachado
animaciones_agachado = []
for i in range(1):
    imagen = pygame.image.load("Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_agachado//mov_agachado_0.png").convert_alpha()
    animaciones_agachado.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_agachado = Weapon(animaciones_agachado)   

        #saltando
        
animaciones_saltando = []
for i in range(1):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//salto_bill//salto_{i}.png").convert_alpha()
    animaciones_saltando.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

saltar = Weapon(animaciones_saltando)           
        
        
# Animaciones para el enemigo 
animaciones_enemigo = []
for i in range(5):
    img = pygame.image.load(f"Recursos//Sprites//Enemigos//enemigos_que_si_se_mueven//enemigo_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones_enemigo.append(img) 
    
animacion_explosion = []
for i in range(5):
    imagen = pygame.image.load(f"Recursos//Sprites//explosiones//explosion_{i}.png").convert_alpha()
    imagen_escalada = escalar_img(imagen, constantes.SCALA_PERSONAJE) 
    animacion_explosion.append(imagen_escalada)
    
    
soltar_power_up = []    
for i in range(1):
    imagen = pygame.image.load("Recursos//Sprites//powerups//suelta_power_ups.png").convert_alpha()
    imagen_escalada = escalar_img(imagen, constantes.SCALA_PERSONAJE)  
    soltar_power_up.append(imagen_escalada)
explosion_actual = None





animaciones_apuntando_izquierda = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_dereha//izquierda//mov_apuntando_izquierda_{i}.png").convert_alpha()
    animaciones_apuntando_izquierda.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_izquierda = Weapon(animaciones_apuntando_izquierda)

animaciones_apuntando_izquierda_izquierda = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_45_derecha//izquierda//mov_45_izquierda_{i}.png").convert_alpha()
    animaciones_apuntando_izquierda_izquierda.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_izquierda_izquierda = Weapon(animaciones_apuntando_izquierda_izquierda)

animaciones_apuntando_izquierda_abajo = []
for i in range(2):
    imagen = pygame.image.load(f"Recursos//Sprites//Bill_y_Lance//Bill(azul)//mov_apuntando_bill//mov_apuntando_315_derecha//izquierda//mov_315_izquierda_{i}.png").convert_alpha()
    animaciones_apuntando_izquierda_abajo.append(escalar_img(imagen, constantes.SCALA_PERSONAJE))

apuntar_abajo_izquierda = Weapon(animaciones_apuntando_izquierda_abajo)



# fuentes
font_inicio = pygame.font.Font("Recursos//letra//PressStart2P-Regular.ttf", 25)
font_titulo = pygame.font.Font("Recursos//letra//PressStart2P-Regular.ttf", 25)

#Botones 
boton_jugar1p = pygame.Rect(100, 470, 200, 50)
boton_salir = pygame.Rect(100,540, 200, 50)

boton_controles = pygame.Rect(540, 500, 200, 50)

boton_regresar = pygame.Rect(540, 500, 250, 50)

boton_siguiente = pygame.Rect(540, 450, 250, 50)

# texto_boton_jugar = font_inicio.render("1 Player", True, constantes.BLANCO)
# Texto
texto_boton_salir = font_inicio.render("Salir", True, constantes.BLANCO)

texto_regresar = font_inicio.render("regresar", True, constantes.BLANCO)

texto_siguiente = font_inicio.render("Siguiente", True, constantes.BLANCO)

texto_boton_controles = font_inicio.render("Controles", True, constantes.BLANCO)
def pantalla_inicio():
    screen.fill((30, 30, 30))
    start_Button.draw()
    # pygame.draw.rect(screen,constantes.COLOR_BG, boton_jugar1p)
    pygame.draw.rect(screen,constantes.COLOR_BG, boton_salir)
    pygame.draw.rect(screen,constantes.COLOR_BG, boton_controles)
    # texto botones
    # screen.blit(texto_boton_jugar, (boton_jugar1p.x + 50, boton_jugar1p.y + 10))
    screen.blit(texto_boton_salir, (boton_salir.x + 30, boton_salir.y + 10))
    screen.blit(texto_boton_controles,(boton_controles.x + 30, boton_controles.y + 10))

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
    
    
    
    jugador = Personaje(100, 300, animaciones_sin_apuntar)
    
    
    pygame.display.set_caption("Controles")
    
       
    diccionario_armas = {
        "arriba": apuntar_arriba,
        "derecha": apuntar_derecha,
        "derecharecto": apuntar_derecha_recto,
        "derechaabajo": apuntar_derecha_abajo,
        "abajo": apuntar_agachado,
        "saltar": saltar,
        "nada": nada,
        "izquierda": apuntar_izquierda ,
        "izquierda_arriba":apuntar_izquierda_izquierda ,
        "izquierda_abajo": apuntar_abajo_izquierda
    }
    
    direccion_apuntado = None
    ultima_direccion_arma = None  
    
    
    pygame.display.set_caption("Controles")
    
    
    mover_arriba = False
    mover_abajo = False
    mover_derecha = False
    mover_izquierda = False
    tecla_i_presionada = False
    tecla_l_presionada = False
    tecla_j_presionada = False
    tecla_k_presionada = False
    tecla_m_presionada = False
    tecla_espacio_presionada = False
    ninguna_tecla_presionada = False
    
    
    arriba = False
    agachado = False
    posicion_original_y = jugador.shape.y  
    posicion_original_x = jugador.shape.x
    
    posicion_original_y_arriba = jugador.shape.y  
    posicion_original_x_arriba = jugador.shape.x
    
    clock = pygame.time.Clock()
    
    
    while run == True:
        screen.fill((30, 30, 30))
        fuente = pygame.font.Font(None, 36)
        texto = font_inicio.render("CONTROLES", True, (25, 255, 255))
        screen.blit(texto, (300, 50))
        texto = font_inicio.render("← A | D →", True, (25, 255, 255))
        screen.blit(texto, (50, 100))
        screen.blit(animaciones_sin_apuntar[0], (100,200))
        screen.blit(animaciones_sin_apuntar[1], (200,200))
        
        texto = font_inicio.render("l+m", True, (25, 255, 255))
        screen.blit(texto, (325, 100))
        screen.blit(animaciones_apuntando_derecha_abajo[0], (350,200))
        
        texto = font_inicio.render("   ↓ k", True, (25, 255, 255))
        screen.blit(texto, (380, 100))
        screen.blit(animaciones_agachado[0], (480,230))
        
        texto = font_inicio.render("   ↑ Espacio", True, (25, 255, 255))
        screen.blit(texto, (500, 100))
        screen.blit(animaciones_saltando[0], (650,200))
        
        
        
        
        texto = font_inicio.render("↑ i", True, (25, 255, 255))
        screen.blit(texto, (50, 400))
        screen.blit(animaciones_apuntando_arriba[0], (100,450))
        
        
        
        texto = font_inicio.render("i + k", True, (25, 255, 255))
        screen.blit(texto, (200, 400))
        screen.blit(animaciones_apuntando_derecha[0], (250,470))
        
        texto = font_inicio.render("← k →", True, (25, 255, 255))
        screen.blit(texto, (400, 400))
        screen.blit(animaciones_apuntando_derecha_bien_derecha[0], (400,470))
        
        
        
        
        
        pygame.draw.rect(screen,constantes.COLOR_BG, boton_siguiente)
        screen.blit(texto_siguiente , (boton_siguiente.x + 30, boton_siguiente.y + 10))
        pygame.draw.rect(screen,constantes.COLOR_BG, boton_regresar)
        screen.blit(texto_regresar , (boton_regresar.x + 30, boton_regresar.y + 10))
        mouse_pos = pygame.mouse.get_pos()
        if boton_regresar.collidepoint(mouse_pos): 
            screen.blit(icono, (boton_regresar.left - icono.get_width() - 10, boton_regresar.centery - icono.get_height() // 2))
        if boton_siguiente.collidepoint(mouse_pos): 
            screen.blit(icono, (boton_siguiente.left - icono.get_width() - 10, boton_siguiente.centery - icono.get_height() // 2))
            
        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.collidepoint(event.pos):
                    fade(screen)
                    inicio()
                if boton_siguiente.collidepoint(event.pos):
                    fade(screen)
                    pantalla_controles_disparo()
                
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                # Disparo
                if event.key == pygame.K_c:
                    nuevo_disparo = Disparo(jugador.shape.centerx, jugador.shape.centery, direccion_apuntado, sprites_disparo["bala_1"])
                    disparos.add(nuevo_disparo)
                    print("c")
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_i and not tecla_j_presionada :
                    tecla_i_presionada = True
                    if not arriba:
                        posicion_original_y_arriba = jugador.shape.y 
                        jugador.shape.y -= 20
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = True
                if event.key == pygame.K_k:
                    tecla_k_presionada = True
                if event.key == pygame.K_j:
                    tecla_j_presionada = True
                    if not agachado:
                        posicion_original_y = jugador.shape.y 
                        jugador.shape.y += 20  
                        agachado = True
                if event.key == pygame.K_SPACE:
                    if not diccionario_armas["saltar"].modo_temporal: 
                        tecla_espacio_presionada = True
                        diccionario_armas["saltar"].activar_modo_temporal()
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_i:
                    tecla_i_presionada = False
                    if arriba:
                        jugador.shape.y = jugador.shape.y  
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
                if event.key == pygame.K_k:
                    tecla_k_presionada = False
                if event.key == pygame.K_j:
                    tecla_j_presionada = False
                    if agachado:
                        jugador.shape.y = jugador.shape.y
                        agachado = True
                if event.key == pygame.K_SPACE:
                    tecla_espacio_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
    
        
        
        
        # Estos son los ejes
        delta_x = 0
        delta_y = 0
        if direccion_apuntado != "arriba":
            if mover_derecha:
                delta_x = constantes.VELOCIDAD
            if mover_izquierda:
                delta_x = -constantes.VELOCIDAD
            if mover_arriba:
                delta_y = -constantes.VELOCIDAD
            if mover_abajo:
                delta_y = constantes.VELOCIDAD
        
        # Bordes
        if jugador.shape.left < 50:
            jugador.shape.left = 50
        if jugador.shape.right > constantes.ANCHO - 10:
            jugador.shape.right = constantes.ANCHO - 10
        
        
        if agachado:
            jugador.shape.y = posicion_original_y + 20
            
        else:
            jugador.shape.y = posicion_original_y 
        
        #
        jugador.movimiento(delta_x, delta_y)
        
        
        jugador.update()
        
        
        
        
        arma_salto = diccionario_armas["saltar"]
        if tecla_m_presionada and tecla_l_presionada:
            direccion_apuntado = "derechaabajo"
        elif tecla_j_presionada and tecla_i_presionada:
            direccion_apuntado = "izquierda_arriba"
        elif tecla_j_presionada and tecla_m_presionada:
            direccion_apuntado = "izquierda_abajo"
        elif tecla_i_presionada and tecla_l_presionada:
            direccion_apuntado = "derecha"
        elif tecla_espacio_presionada:
            direccion_apuntado = "saltar"
        elif tecla_i_presionada:
            direccion_apuntado = "arriba"
        elif tecla_j_presionada:
            direccion_apuntado = "izquierda"
        elif tecla_l_presionada:
            direccion_apuntado = "derecharecto"
        elif tecla_k_presionada:
            direccion_apuntado = "abajo"
        else:
            direccion_apuntado = None
            # direccion_apuntado = "nada"
        print("Dirección de apuntado:", direccion_apuntado)
        
        
        arma_salto = diccionario_armas["saltar"]
        if arma_salto.modo_temporal:
            arma_salto.update(jugador)
            arma_salto.dibujar(screen)
        else:
            if direccion_apuntado:
                ultima_direccion_arma = direccion_apuntado
            
            arma_a_dibujar = diccionario_armas.get(ultima_direccion_arma)
            if arma_a_dibujar:
                arma_a_dibujar.update(jugador)
                arma_a_dibujar.dibujar(screen)
            else:
                jugador.draw(screen)
        
        disparos.update()
        disparos.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

    
    

boton_atras = pygame.Rect(100,540, 200, 50)



def pantalla_controles_disparo():
    
    
   

    
    jugador = Personaje(100, 300, animaciones_sin_apuntar)
    
    
    pygame.display.set_caption("Controles")
    
       
    diccionario_armas = {
        "arriba": apuntar_arriba,
        "derecha": apuntar_derecha,
        "derecharecto": apuntar_derecha_recto,
        "derechaabajo": apuntar_derecha_abajo,
        "abajo": apuntar_agachado,
        "saltar": saltar,
        "nada": nada,
        "izquierda": apuntar_izquierda ,
        "izquierda_arriba":apuntar_izquierda_izquierda ,
        "izquierda_abajo": apuntar_abajo_izquierda
    }
    
    direccion_apuntado = None
    ultima_direccion_arma = None  
    
    
    pygame.display.set_caption("Controles")
    
   
    mover_arriba = False
    mover_abajo = False
    mover_derecha = False
    mover_izquierda = False
    tecla_i_presionada = False
    tecla_l_presionada = False
    tecla_j_presionada = False
    tecla_k_presionada = False
    tecla_m_presionada = False
    tecla_espacio_presionada = False
    ninguna_tecla_presionada = False
    
    
    arriba = False
    agachado = False
    posicion_original_y = jugador.shape.y  
    posicion_original_x = jugador.shape.x
    
    posicion_original_y_arriba = jugador.shape.y  
    posicion_original_x_arriba = jugador.shape.x
    
    clock = pygame.time.Clock()
    
    
    while run == True:
        screen.fill((30, 30, 30))
        fuente = pygame.font.Font(None, 36)
        texto = font_inicio.render("CONTROLES", True, (25, 255, 255))
        screen.blit(texto, (300, 50))
        texto = font_inicio.render("Dispara con c", True, (25, 255, 255))
        screen.blit(texto, (30, 100))
        screen.blit(animaciones_apuntando_izquierda[0], (0,0))
        
        
        texto = font_inicio.render("Prueba en todas direcciones con", True, (25, 255, 255))
        screen.blit(texto, (30, 150))
        
        texto = font_inicio.render("i l k m j", True, (25, 255, 255))
        screen.blit(texto, (30, 200))
        
        
        
        
        
        
        
        pygame.draw.rect(screen,constantes.COLOR_BG, boton_regresar)
        screen.blit(texto_regresar , (boton_regresar.x + 30, boton_regresar.y + 10))
        mouse_pos = pygame.mouse.get_pos()
        
        if boton_regresar.collidepoint(mouse_pos): 
            screen.blit(icono, (boton_regresar.left - icono.get_width() - 10, boton_regresar.centery - icono.get_height() // 2))
            
        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.collidepoint(event.pos):
                    fade(screen)
                    inicio()
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_c:
                    nuevo_disparo = Disparo(jugador.shape.centerx, jugador.shape.centery, direccion_apuntado, sprites_disparo["bala_1"])
                    disparos.add(nuevo_disparo)
                    print("c")
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_i and not tecla_j_presionada :
                    tecla_i_presionada = True
                    if not arriba:
                        posicion_original_y_arriba = jugador.shape.y 
                        jugador.shape.y -= 20
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = True
                if event.key == pygame.K_k:
                    tecla_k_presionada = True
                if event.key == pygame.K_j:
                    tecla_j_presionada = True
                    if not agachado:
                        posicion_original_y = jugador.shape.y 
                        jugador.shape.y += 20  
                        agachado = True
                if event.key == pygame.K_SPACE:
                    if not diccionario_armas["saltar"].modo_temporal: 
                        tecla_espacio_presionada = True
                        diccionario_armas["saltar"].activar_modo_temporal()
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_i:
                    tecla_i_presionada = False
                    if arriba:
                        jugador.shape.y = jugador.shape.y  
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
                if event.key == pygame.K_k:
                    tecla_k_presionada = False
                if event.key == pygame.K_j:
                    tecla_j_presionada = False
                    if agachado:
                        jugador.shape.y = jugador.shape.y
                        agachado = True
                if event.key == pygame.K_SPACE:
                    tecla_espacio_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
    
        
        
        
        
        delta_x = 0
        delta_y = 0
        if direccion_apuntado != "arriba":
            if mover_derecha:
                delta_x = constantes.VELOCIDAD
            if mover_izquierda:
                delta_x = -constantes.VELOCIDAD
            if mover_arriba:
                delta_y = -constantes.VELOCIDAD
            if mover_abajo:
                delta_y = constantes.VELOCIDAD
        
        # Bordes
        if jugador.shape.left < 50:
            jugador.shape.left = 50
        if jugador.shape.right > constantes.ANCHO - 10:
            jugador.shape.right = constantes.ANCHO - 10
        
        
        if agachado:
            jugador.shape.y = posicion_original_y + 20
            
        else:
            jugador.shape.y = posicion_original_y 
        
       
        jugador.movimiento(delta_x, delta_y)
        
        
        jugador.update()
        
        
        
        
        arma_salto = diccionario_armas["saltar"]
        if tecla_m_presionada and tecla_l_presionada:
            direccion_apuntado = "derechaabajo"
        elif tecla_j_presionada and tecla_i_presionada:
            direccion_apuntado = "izquierda_arriba"
        elif tecla_j_presionada and tecla_m_presionada:
            direccion_apuntado = "izquierda_abajo"
        elif tecla_i_presionada and tecla_l_presionada:
            direccion_apuntado = "derecha"
        elif tecla_espacio_presionada:
            direccion_apuntado = "saltar"
        elif tecla_i_presionada:
            direccion_apuntado = "arriba"
        elif tecla_j_presionada:
            direccion_apuntado = "izquierda"
        elif tecla_l_presionada:
            direccion_apuntado = "derecharecto"
        elif tecla_k_presionada:
            direccion_apuntado = "abajo"
        else:
            direccion_apuntado = None
            # direccion_apuntado = "nada"
        print("Dirección de apuntado:", direccion_apuntado)
        
        
        arma_salto = diccionario_armas["saltar"]
        if arma_salto.modo_temporal:
            arma_salto.update(jugador)
            arma_salto.dibujar(screen)
        else:
            if direccion_apuntado:
                ultima_direccion_arma = direccion_apuntado
            
            arma_a_dibujar = diccionario_armas.get(ultima_direccion_arma)
            if arma_a_dibujar:
                arma_a_dibujar.update(jugador)
                arma_a_dibujar.dibujar(screen)
            else:
                jugador.draw(screen)
        
        disparos.update()
        disparos.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

    
    

boton_atras = pygame.Rect(100,540, 200, 50)

        
            
def juego():
    
    jugador = Personaje(100, 225, animaciones_sin_apuntar)
    enemigo1 = Enemigos.Enemigo(400, 225, animaciones_enemigo)
    suelta_power_ups = PowerUp(50, 50, soltar_power_up)
    
    background = pygame.image.load("Recursos//Sprites//Stage_1//NES - Contra - Stage 1.png").convert()
    screen.blit(background, (0, 0))
   
    pygame.display.update()
        
    diccionario_armas = {
        "arriba": apuntar_arriba,
        "derecha": apuntar_derecha,
        "derecharecto": apuntar_derecha_recto,
        "derechaabajo": apuntar_derecha_abajo,
        "abajo": apuntar_agachado,
        "saltar": saltar,
        "nada": nada,
        "izquierda": apuntar_izquierda ,
        "izquierda_arriba":apuntar_izquierda_izquierda ,
        "izquierda_abajo": apuntar_abajo_izquierda
    }
    
    
    direccion_apuntado = None
    ultima_direccion_arma = None
    
    
    pygame.display.set_caption("Contra")
    
    
    mover_arriba = False
    mover_abajo = False
    mover_derecha = False
    mover_izquierda = False
    tecla_i_presionada = False
    tecla_l_presionada = False
    tecla_j_presionada = False
    tecla_k_presionada = False
    tecla_m_presionada = False
    tecla_espacio_presionada = False
    ninguna_tecla_presionada = False
    
    
    arriba = False
    agachado = False
    posicion_original_y = jugador.shape.y  
    posicion_original_x = jugador.shape.x
    
    posicion_original_y_arriba = jugador.shape.y  
    posicion_original_x_arriba = jugador.shape.x
    
    
    
    
    clock = pygame.time.Clock()
    
    menu_opcion = 0
    
    ultima_direccion_arma = "derecharecto"
    
    estado = "inicio"
    mostrar_controles = False
    mostrar_inicio = True
    run = True
    scroll_x = 0 
    enemigo1.alive = True
    enemigo1.vida = 3
    muertos = 0
    max_muertos = 5
    victoria = False
    jugador.vel_y = 0
    gravedad = 0.5
    
    def respawn_enemigo(enemigo):
        import random
        enemigo.shape.center = (random.randint(100, 400), random.randint(100, 300))
        enemigo.vida = 3
        enemigo.alive = True
    
    while run == True:
   
        
        pygame.mixer.music.stop()
        
    
       
        screen.blit(fondo, (-scroll_x, 0))
        
        
        jugador.vel_y += gravedad
        jugador.shape.y += int(jugador.vel_y)
        # Estos son los ejes
        delta_x = 0
        delta_y = 0
        
        if direccion_apuntado != "arriba":
            if mover_derecha:
                delta_x = constantes.VELOCIDAD
            if mover_izquierda:
                delta_x = -constantes.VELOCIDAD
            if mover_arriba:
                delta_y = -constantes.VELOCIDAD
            if mover_abajo:
                delta_y = constantes.VELOCIDAD
        
        # Bordes
        if jugador.shape.left < 50:
            jugador.shape.left = 50
        if jugador.shape.right > constantes.ANCHO - 10:
            jugador.shape.right = constantes.ANCHO - 10
        
        
        if agachado:
            jugador.shape.y = posicion_original_y + 20
            
        else:
            jugador.shape.y = posicion_original_y 
        
        
        jugador.movimiento(delta_x, delta_y)
        
        
        jugador.update()
        
        
        
       
        if mover_derecha == True:
            delta_x = constantes.VELOCIDAD
        if mover_izquierda == True:
            delta_x = -constantes.VELOCIDAD
        if mover_arriba == True:
            delta_y = -constantes.VELOCIDAD
        if mover_abajo == True:
            delta_y = constantes.VELOCIDAD
        if jugador.shape.left < 50:
            jugador.shape.left = 50
        if jugador.shape.right > constantes.ANCHO - 10:
            jugador.shape.right = constantes.ANCHO - 10
            
        explosion_actual = None
        # Colisión entre bala y enemigo
        
        if not victoria:
            for bala in disparos:
                if bala.rect.colliderect(enemigo1.shape) and enemigo1.alive:
                    enemigo1.vida -= 1
                    disparos.remove(bala)
                    if enemigo1.vida <= 0:
                        if explosion_actual is None or not explosion_actual.activa:
                            explosion_actual = Explosion(enemigo1.shape.centerx, enemigo1.shape.centery, animacion_explosion)
                        enemigo1.alive = False
                        muertos += 1
                    break  
                # Valorar si muere el enemigo
            if jugador.shape.colliderect(enemigo1.shape) and enemigo1.alive:
                if explosion_actual is None or not explosion_actual.activa:
                    explosion_actual = Explosion(enemigo1.shape.centerx, enemigo1.shape.centery, animacion_explosion)
                enemigo1.alive = False
                # Eplosion al morir el enemigo
            if explosion_actual and explosion_actual.activa:
                explosion_actual.update()
                explosion_actual.draw(screen)
            else:
                explosion_actual = None
        
            if enemigo1.alive:
                enemigo1.update()
                enemigo1.perseguir(jugador)
                enemigo1.draw(screen)
            else:
                # Reespawn de enemigo
                if explosion_actual is None or not explosion_actual.activa:
                    if muertos < max_muertos:
                        respawn_enemigo(enemigo1)
                    else:
                        victoria = True
        # Victoria texto
        else:
            font_victoria = pygame.font.Font(None, 72)
            texto = font_victoria.render("¡GANASTE!", True, (0, 255, 0))
            texto2 = font_victoria.render("¡ERES MUY INTELIGENTE!", True, (0, 255, 0))
            screen.blit(texto, (300, 250))
            screen.blit(texto2, (70, 300))
        
        if agachado:
            jugador.shape.y = posicion_original_y + 20
        else:
            jugador.shape.y = posicion_original_y 
        
    
        
        jugador.movimiento(delta_x, delta_y)
                                # HAY QUE ARREGLAR LAS COLISIONES POR QUE SE VA HACIA ABAJO
        # jugador.vel_y += gravedad  # Define tu valor de gravedad si no lo has hecho, por ejemplo: gravedad = 1
        # jugador.shape.y += jugador.vel_y
        
        # # Ver si el jugador está presionando abajo
        # teclas = pygame.key.get_pressed()
        # presionando_abajo = teclas[pygame.K_DOWN] or teclas[pygame.K_s]
        
        # # Suponemos que el jugador no está en el suelo hasta que se verifique lo contrario
        # jugador.en_suelo = False
        
        # # Comprobar colisiones con plataformas
        # for plataforma, tipo in rects_colision:
        #     if tipo == 1:  # Solo plataformas semisólidas
        #         if jugador.shape.colliderect(plataforma):
        #             # Si está cayendo y tocando la parte superior de la plataforma
        #             if jugador.vel_y > 0 and jugador.shape.bottom <= plataforma.top + 10:
        #                 if not presionando_abajo:
        #                     jugador.shape.bottom = plataforma.top
        #                     jugador.vel_y = 0
        #                     jugador.en_suelo = True
        #             # Si está subiendo y choca con la parte de abajo (opcional)
        #             elif jugador.vel_y < 0 and jugador.shape.top >= plataforma.bottom - 10:
        #                 jugador.shape.top = plataforma.bottom
        #                 jugador.vel_y = 0
        
        
        if mover_derecha:
            scroll_x += constantes.VELOCIDAD_SCROLL
        if mover_izquierda and scroll_x > 0:
            scroll_x -= constantes.VELOCIDAD_SCROLL
        
        jugador.update()
        enemigo1.update()
        suelta_power_ups.update()
        
        
        suelta_power_ups.perseguir(jugador)
        suelta_power_ups.draw(screen)
        enemigo1.perseguir(jugador)  
        enemigo1.draw(screen)
    
        # Lógica para apuntar en diferentes direcciones
        teclas = pygame.key.get_pressed()
        
        # Apuntar combinaciones
        if teclas[pygame.K_m] and teclas[pygame.K_l]:
            direccion_apuntado = "derechaabajo"
        elif teclas[pygame.K_j] and teclas[pygame.K_i]:
            direccion_apuntado = "izquierda_arriba"
        elif teclas[pygame.K_j] and teclas[pygame.K_m]:
            direccion_apuntado = "izquierda_abajo"
        elif teclas[pygame.K_i] and teclas[pygame.K_l]:
            direccion_apuntado = "derecha"
        elif teclas[pygame.K_i]:
            direccion_apuntado = "arriba"
        elif teclas[pygame.K_j]:
            direccion_apuntado = "izquierda"
        elif teclas[pygame.K_l]:
            direccion_apuntado = "derecharecto"
        elif teclas[pygame.K_k]:
            direccion_apuntado = "abajo"
        elif teclas[pygame.K_SPACE]:
            direccion_apuntado = "saltar"
        else:
            direccion_apuntado = None
    
        
        arma_actual = diccionario_armas.get(direccion_apuntado)
    
        
        arma_salto = diccionario_armas["saltar"]
        if arma_salto.modo_temporal:
            arma_salto.update(jugador)
            arma_salto.dibujar(screen)
        else:
            
            if direccion_apuntado:
                ultima_direccion_arma = direccion_apuntado
    
            
            arma_a_dibujar = diccionario_armas.get(ultima_direccion_arma)
            if arma_a_dibujar:
                arma_a_dibujar.update(jugador)
                arma_a_dibujar.dibujar(screen)
            else:
                jugador.draw(screen)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.KEYDOWN:
                
                   # Disparo
                if event.key == pygame.K_c:
                    nuevo_disparo = Disparo(jugador.shape.centerx, jugador.shape.centery, direccion_apuntado, sprites_disparo["bala_1"])
                    disparos.add(nuevo_disparo)
                    print("c")
                    
                if event.key == pygame.K_a:
                    mover_izquierda = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_i and not tecla_j_presionada:
                    tecla_i_presionada = True
                    if not arriba:
                        posicion_original_y_arriba = jugador.shape.y 
                        jugador.shape.y -= 20
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = True
                if event.key == pygame.K_k:
                    tecla_k_presionada = True
                    if not agachado:
                        posicion_original_y = jugador.shape.y 
                        jugador.shape.y += 20  
                        agachado = True
                if event.key == pygame.K_SPACE:
                    if not diccionario_armas["saltar"].modo_temporal: 
                        tecla_espacio_presionada = True
                        diccionario_armas["saltar"].activar_modo_temporal()
        
                    
                    
    
    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_i:
                    tecla_i_presionada = False
                    if arriba:
                        jugador.shape.y = jugador.shape.y  
                        arriba = True
                if event.key == pygame.K_l:
                    tecla_l_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = True
                if event.key == pygame.K_m:
                    tecla_m_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
                if event.key == pygame.K_k:
                    tecla_k_presionada = False
                    if agachado:
                        jugador.shape.y = jugador.shape.y
                        agachado = True
                if event.key == pygame.K_SPACE:
                    tecla_espacio_presionada = False
                    if arriba:
                        jugador.shape.y = posicion_original_y  
                        arriba = False
            if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()
               boton_regresar = pygame.Rect(50, 550, 250, 50)
               if boton_regresar.collidepoint(mouse_pos):
                   fade(screen)
                   inicio()
                
                
    
        boton_regresar = pygame.Rect(50, 550, 250, 50)
        texto_regresar = font_inicio.render("regresar", True, constantes.BLANCO)
        pygame.draw.rect(screen,constantes.COLOR_BG, boton_regresar)
        screen.blit(texto_regresar , (boton_regresar.x + 30, boton_regresar.y + 10))
        mouse_pos = pygame.mouse.get_pos()
        if boton_regresar.collidepoint(mouse_pos): 
            screen.blit(icono, (boton_regresar.left - icono.get_width() - 10, boton_regresar.centery - icono.get_height() // 2))   
           
            
    
    
    
        
                
        
        
        disparos.update()
        disparos.draw(screen)
        
        pygame.display.update()
        
        clock.tick(60)
        
        pygame.display.update()


clock = pygame.time.Clock()
# Esto llama a todo el juego, hay que ponerlo en otro archivo y que sea el principal
def inicio():
    run = True 
    estado = "inicio"
    mostrar_controles = False
    mostrar_inicio = True
    while run: 
        
        
        if mostrar_inicio == True:
             for event in pygame.event.get():
                 
                 if event.type == pygame.QUIT:
                     run = False
                 if event.type == pygame.MOUSEBUTTONDOWN:
                     
                     if boton_jugar1p.collidepoint(event.pos): 
                         fade(screen)
                         estado = "juego"
                     if boton_salir.collidepoint(event.pos):
                         fade(screen)
                         run = False
                 if event.type == pygame.MOUSEBUTTONDOWN:
                     if boton_controles.collidepoint(event.pos):
                         
                         estado = "controles"
                         fade(screen)
                 if event.type == pygame.MOUSEBUTTONDOWN:
                     if boton_siguiente.collidepoint(event.pos):
                        
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
             if estado == "controles_apuntar":
                 pantalla_controles_disparo()
                 
                 
                
             if estado == "juego":
                juego()
             
                 
            
                 
                   
                 
                 
             pygame.display.update()
             clock.tick(60) 
    pygame.quit()
    sys.exit()

    

inicio()
pygame.quit()
sys.exit()


    