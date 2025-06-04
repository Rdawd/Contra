import pygame
import csv
import sys

# Inicializar Pygame
pygame.init()

# Configuración ventana
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Colisiones invisibles desde CSV")

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
        if celda == 1:
            x = col_idx * TILE_SIZE
            y = fila_idx * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            rects_colision.append(rect)

# Bucle principal Pygame
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    screen.fill((0, 0, 0))


    pygame.display.flip()

pygame.quit()
sys.exit()


