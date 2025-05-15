import pygame
import sys
import constantes
from personajes import Personaje
from weapons import Weapon

# Esto indica que iniciara el juego a partir de aqui
pygame.init()
# Esto crea la ventana usando el ancho y alto determinado en constantes, aunque podria poner 600, 400 y funcionaria igual
screen = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size=(w * scale, h * scale))
    return nueva_imagen

# recorro las imagenes 1 por 1, todas las que necesito
    # personaje
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

apuntar_derecha = Weapon(animaciones_apuntando_derecha)  # <-- corregido: pasamos la lista completa

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
        
        
        
        
        
        

# 50, 50 es el lugar donde esta apareciendo el  o jugador personaje el cual se esta creando en personajes y luego lo importo. Tengo que igualarlo a una variable de aca para que funcione sin problemas
jugador = Personaje(50, 50, animaciones_sin_apuntar)

# Diccionario de armas para diferentes direcciones
diccionario_armas = {
    "arriba": apuntar_arriba,
    "derecha": apuntar_derecha,
    "derecharecto": apuntar_derecha_recto,
    "derechaabajo": apuntar_derecha_abajo,
    "abajo": apuntar_agachado
    # puedes agregar más direcciones aquí
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

# Esto permite crear la variable clock que determina los fps a los que se mueve el juego para no saturar la maquina
clock = pygame.time.Clock()
while True:

    # El color screen.fill hace que cada frame que se mueve sustituya por el color del fondo
    screen.fill(constantes.COLOR_BG)
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
    # Aqui se le reemplaza los valores de x y y al movimiento
    jugador.movimiento(delta_x, delta_y)

    # actualiza el jugador
    jugador.update()

    # Lógica para apuntar en diferentes direcciones
    
    if tecla_m_presionada and tecla_l_presionada:
        direccion_apuntado = "derechaabajo"
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
    print("Dirección de apuntado:", direccion_apuntado)

    # Dibujamos el arma si hay direccion de apuntado
    if direccion_apuntado in diccionario_armas:
        diccionario_armas[direccion_apuntado].update(jugador)
        diccionario_armas[direccion_apuntado].dibujar(screen)
    else:
        jugador.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_i:
                tecla_i_presionada = True
            if event.key == pygame.K_l:
                tecla_l_presionada = True
            if event.key == pygame.K_m:
                tecla_m_presionada = True
            if event.key == pygame.K_k:
                tecla_k_presionada = True

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
            if event.key == pygame.K_l:
                tecla_l_presionada = False
            if event.key == pygame.K_m:
                tecla_m_presionada = False
            if event.key == pygame.K_k:
                tecla_k_presionada = False

    # hace que se actualice la pantalla para mostrar la nueva imagen y no se quede estática
    pygame.display.update()
    # permite poner los fps
    clock.tick(60)
    # lo mismo que la otra de arriba pero por si acaso no la quites
    pygame.display.update()
