import pygame
class Explosion:
    def __init__(self, x, y, frames, escala=1, tiempo_por_frame=5):
        self.alive = True
        self.frames = frames
        self.frame_actual = 0
        self.tiempo_por_frame = tiempo_por_frame
        self.tiempo_contador = 0
        self.activa = True
        
        self.x = x
        self.y = y
        
        self.rect = self.frames[0].get_rect(center=(x, y))

    def update(self):
        if not self.activa:
            return
        self.tiempo_contador += 1
        if self.tiempo_contador >= self.tiempo_por_frame:
            self.tiempo_contador = 0
            self.frame_actual += 1
            if self.frame_actual >= len(self.frames):
                self.activa = False  

    def draw(self, screen):
        if self.activa:
            screen.blit(self.frames[self.frame_actual], self.rect)