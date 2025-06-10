import pygame
import math

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, imagen, tipo="bala_1", mirar_izquierda=False, tiempo_maximo=5000):
        super().__init__()
        
        self.tipo = tipo  # Guardamos el tipo de bala
        self.image = pygame.transform.flip(imagen, True, False) if mirar_izquierda else imagen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direccion = direccion
        self.velocidad = 8

        # Define el daño según el tipo de bala
        self.daño = 1 if tipo == "bala_1" else 3  

       
        self.tiempo_inicio = pygame.time.get_ticks()
        self.tiempo_maximo = tiempo_maximo  

        # Direccion de la bala según el diccionario de armas
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
            angulo = math.radians(225)
            self.vel_x = math.cos(angulo) * self.velocidad
            self.vel_y = math.sin(angulo) * self.velocidad
        elif direccion == "izquierda_abajo":
            angulo = math.radians(225)
            self.vel_x = math.cos(angulo) * self.velocidad
            self.vel_y = -math.sin(angulo) * self.velocidad
        else:
            self.vel_x = self.velocidad
            self.vel_y = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_inicio > self.tiempo_maximo:
            self.kill()