import pygame
import sys
import constantes
import Enemigos
from Powerups import PowerUp
from explosiones import Explosion
from personajes import Personaje
from weapons import Weapon

# Esto indica que iniciara el juego a partir de aqui
pygame.init()
# Esto crea la ventana usando el ancho y alto determinado en constantes, aunque podria poner 600, 400 y funcionaria igual, solo cambiandolo de constantes tambien hace la escala del fondo
screen = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
scroll_x = 0





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
inicio = pygame.mixer.music.set_volume(0.1)
inicio = pygame.mixer.music.play(-1)
  

# recorro las imagenes 1 por 1, todas las que necesito
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

    # Balas
balas_basicas = []
    
for i in range(1):
    imagen_bala = pygame.image.load(f"Recursos//Sprites//Disparos//disparo_basico.png").convert_alpha()
    imagen_bala = escalar_img(img, constantes.SCALA_PERSONAJE)
    balas_basicas.append(imagen_bala)
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

# fuentes
font_inicio = pygame.font.Font("Recursos//letra//PressStart2P-Regular.ttf", 25)
font_titulo = pygame.font.Font("Recursos//letra//PressStart2P-Regular.ttf", 25)

#Botones de inicio
boton_jugar1p = pygame.Rect(constantes.ANCHO / 2 - 100, constantes.ALTO / 2 - 50, 200, 50)
boton_salir = pygame.Rect(constantes.ANCHO / 2 - 100, constantes.ALTO / 2 + 50, 200, 50)

texto_boton_jugar = font_inicio.render("1 Player", True, constantes.BLANCO)
texto_boton_salir = font_inicio.render("Salir", True, constantes.BLANCO)

def pantalla_inicio():
    screen.blit(pantalla_de_inicio,(0,0))
dibujar_texto("CONTRA", font_titulo, constantes.BLANCO, constantes.ANCHO/ 2 - 200+150,constantes.ALTO / 2 - 200,constantes.SCALA_PERSONAJE)
pygame.draw.rect(screen,constantes.COLOR_BG, boton_jugar1p)
pygame.draw.rect(screen,constantes.COLOR_BG, boton_salir)
screen.blit(texto_boton_jugar, (boton_jugar1p.x + 50, boton_jugar1p.y + 10))
screen.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
pygame.display.update()




        
        

# 100, 225 es el lugar donde esta apareciendo el  o jugador personaje el cual se esta creando en personajes y luego lo importo. Tengo que igualarlo a una variable de aca para que funcione sin problemas
jugador = Personaje(100, 225, animaciones_sin_apuntar)
enemigo1 = Enemigos.Enemigo(400, 225, animaciones_enemigo)
suelta_power_ups = PowerUp(50, 50, soltar_power_up)

background = pygame.image.load("Recursos//Sprites//Stage_1//NES - Contra - Stage 1.png").convert()
screen.blit(background, (0, 0))


 # Aqui SOLOOOO van las direcciones del arma
diccionario_armas = {
    "arriba": apuntar_arriba,
    "derecha": apuntar_derecha,
    "derecharecto": apuntar_derecha_recto,
    "derechaabajo": apuntar_derecha_abajo,
    "abajo": apuntar_agachado,
    "saltar": saltar,
    "nada": nada
    #
}



direccion_apuntado = None

# Titulo de la ventana
pygame.display.set_caption("GAME TEST")

# Determinamos los movimientos como falsos para que sean true cuando apretemos un boton con la funcion de más adelante
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



# Esto permite crear la variable clock que determina los fps a los que se mueve el juego para no saturar la maquina
clock = pygame.time.Clock()

ultima_direccion_arma = "derecharecto"
mostrar_inicio = True
run = True
while run == True:
    if mostrar_inicio == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar1p.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
            
        
        pantalla_inicio()
    else:
        pygame.mixer.music.stop()
        
    
        # El color screen.fill hace que cada frame que se mueve sustituya por el color del fondo
        screen.blit(fondo, (-scroll_x, 0))
    
        # Estos son los ejes
        delta_x = 0
        delta_y = 0
        
        
        # Aqui lo que haces es darle el valor al que se movera cuando sea true el movimiento, pero aún no lo hacemos true
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
            
        # colision enemigo
        if jugador.shape.colliderect(enemigo1.shape) and enemigo1.alive:
            if explosion_actual is None or not explosion_actual.activa:
                explosion_actual = Explosion(enemigo1.shape.centerx, enemigo1.shape.centery, animacion_explosion)
                enemigo1.alive = False
    
        if explosion_actual and explosion_actual.activa:
            explosion_actual.update()
            explosion_actual.draw(screen)
        else:
            explosion_actual = None
        
        if enemigo1.alive:
            enemigo1.update()
            enemigo1.perseguir(jugador)
            enemigo1.draw(screen)
        
        if agachado:
            jugador.shape.y = posicion_original_y + 20
        else:
            jugador.shape.y = posicion_original_y 
        
    
        # Aqui se le reemplaza los valores de x y y al movimiento
        jugador.movimiento(delta_x, delta_y)
        
        # mueve el fondo con el jugador con el problema de que si voy a la izquierda se pone por 2 la velocidad y no se por que, tiene que ver con la class personajes y no aqui
        if mover_derecha:
            scroll_x += 0.5
        if mover_izquierda and scroll_x > 0:
            scroll_x -= constantes.VELOCIDAD
        # actualiza el jugador
        jugador.update()
        enemigo1.update()
        suelta_power_ups.update()
        
        # Para solucionar que siga al jugador voy a crear otro sprite y lo colocare abajo, y se lo pasare como parametro para que siga a ese sprite
        suelta_power_ups.perseguir(jugador)
        suelta_power_ups.draw(screen)
        enemigo1.perseguir(jugador)  
        enemigo1.draw(screen)
    
        # Lógica para apuntar en diferentes direcciones
        arma_salto = diccionario_armas["saltar"]
    
        
        if tecla_m_presionada and tecla_l_presionada:
            direccion_apuntado = "derechaabajo"
        elif tecla_espacio_presionada:
            direccion_apuntado = "saltar"
        elif tecla_i_presionada and tecla_l_presionada:
            direccion_apuntado = "derecha"
        elif tecla_i_presionada:
            direccion_apuntado = "arriba"
        elif tecla_l_presionada:
            direccion_apuntado = "derecharecto"
        elif tecla_k_presionada:
            direccion_apuntado = "abajo"
        else:
            direccion_apuntado = None
            # direccion_apuntado = "nada"
        print("Dirección de apuntado:", direccion_apuntado)
    
        # Dibujamos el arma si hay direccion de apuntado
        arma_actual = diccionario_armas.get(direccion_apuntado)
    
        # Verifica si el arma del salto está activa
        arma_salto = diccionario_armas["saltar"]
        if arma_salto.modo_temporal:
            arma_salto.update(jugador)
            arma_salto.dibujar(screen)
        else:
            
            if direccion_apuntado:
                ultima_direccion_arma = direccion_apuntado
    
            # Usa la última arma usada si no hay nueva dirección
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
                if event.key == pygame.K_a:
                    mover_izquierda = True
                # if event.key == pygame.K_w:
                #     mover_arriba = True
                # if event.key == pygame.K_s:
                #     mover_abajo = True
                if event.key == pygame.K_d:
                    mover_derecha = True
                if event.key == pygame.K_i:
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
                    # posicion_original_y = jugador.shape.y 
                    # posicion_original_x = jugador.shape.x
                    # jugador.shape.y +=20
                    # Personaje = Personaje(posicion_original_x , posicion_original_y , animaciones_sin_apuntar)
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
                
                
    
            
            
            
    
    
    
        
                
        
        
        
        # hace que se actualice la pantalla para mostrar la nueva imagen y no se quede estática
        pygame.display.update()
        # permite poner los fps
        clock.tick(60)
        # lo mismo que la otra de arriba pero por si acaso no la quites
        pygame.display.update()
pygame.quit()


