import pygame

class Weapon():
    def __init__(self, imagenes_arma):
        self.animaciones = imagenes_arma
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[0]
        self.shape = self.image.get_rect()

        self.modo_temporal = False
        self.tiempo_inicio_modo = 0
        self.duracion_modo_ms = 200  # duración de la animación temporal

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.shape)

    def activar_modo_temporal(self):
        self.modo_temporal = True
        self.tiempo_inicio_modo = pygame.time.get_ticks()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self, jugador):
        cooldown_animacion = 150

        if self.modo_temporal:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio_modo >= self.duracion_modo_ms:
                self.modo_temporal = False

        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()

        
        self.image = self.animaciones[self.frame_index]

        
        self.shape.centerx = jugador.shape.centerx
        self.shape.centery = jugador.shape.centery