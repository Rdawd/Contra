import pygame
import constantes
import math


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, imagen, mirar_izquierda=False):
        super().__init__()
        
        self.image = pygame.transform.flip(imagen, True, False) if mirar_izquierda else imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direccion = direccion
        self.velocidad = 10  # Velocidad del disparo,SIN CONFUSION

        # Direccion de la bala segun el diccionario de armas
        if direccion == "derecha":
            self.vel_x = -self.velocidad * (math.sqrt(2)/2) if mirar_izquierda else self.velocidad * (math.sqrt(2)/2)
            self.vel_y = -self.velocidad * (math.sqrt(2)/2)
        elif direccion == "izquierda":
            self.vel_x = -self.velocidad
            self.vel_y = 0
        elif direccion == "arriba":
            self.vel_x = 0
            self.vel_y = -self.velocidad
        elif direccion == "abajo":
            self.vel_x = -self.velocidad if mirar_izquierda else self.velocidad
            self.vel_y = 0
        elif direccion == "derechaabajo":
            self.vel_x = -self.velocidad * (math.sqrt(2)/2) if mirar_izquierda else self.velocidad * (math.sqrt(2)/2)
            self.vel_y = self.velocidad * (math.sqrt(2)/2)
        elif direccion == "derecharecto":
            self.vel_x = -self.velocidad if mirar_izquierda else self.velocidad
            self.vel_y = 0
        elif direccion == "izquierda_arriba":
            self.vel_x = -self.velocidad / math.sqrt(2)
            self.vel_y = -self.velocidad / math.sqrt(2)
        elif direccion == "izquierda_abajo":
            angulo = math.radians(225)
            self.vel_x = math.cos(angulo) * self.velocidad
            self.vel_y = math.sin(angulo) * self.velocidad
        else:
            self.vel_x = self.velocidad
            self.vel_y = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Eliminar si se sale de la pantalla
        pantalla_ancho, pantalla_alto = pygame.display.get_surface().get_size()
        if (self.rect.right < 0 or self.rect.left > pantalla_ancho or
            self.rect.bottom < 0 or self.rect.top > pantalla_alto):
            self.kill()