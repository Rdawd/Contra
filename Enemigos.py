import pygame

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones, velocidad=2, gravedad=1, vida=3):
        super().__init__()
        self.alive = True
        self.vida = vida  # Cantidad de balas necesarios para eliminar al enemigo

        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.velocidad = velocidad           
        self.gravedad = gravedad             
        self.vel_y = 0                       # Velocidad vertical inicial
        self.flip = True

        self.image = self.animaciones[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def mover_con_colision(self, delta_x, delta_y, rects_colision):
        # Movimiento en X
        self.rect.x += delta_x
        for rect in rects_colision:
            if self.rect.colliderect(rect):
                if delta_x > 0:
                    self.rect.right = rect.left
                elif delta_x < 0:
                    self.rect.left = rect.right

        # Movimiento en Y
        self.rect.y += delta_y
        for rect in rects_colision:
            if self.rect.colliderect(rect):
                if delta_y > 0:  # Colisión al caer
                    self.rect.bottom = rect.top
                    self.vel_y = 0
                elif delta_y < 0:  # Colisión al subir
                    self.rect.top = rect.bottom
                    self.vel_y = 0

    def update(self, rects_colision):
        if not self.alive:
            return

        # Actualización de animación
        cooldown_animacion = 100  # milisegundos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = tiempo_actual
        self.image = self.animaciones[self.frame_index]

        # Movimiento horizontal hacia la izquierda)
        self.mover_con_colision(-self.velocidad, 0, rects_colision)

        # Aplicar gravedad
        self.vel_y += self.gravedad
        if self.vel_y > 10:
            self.vel_y = 10  # Limitar la velocidad máxima de caida
        self.mover_con_colision(0, self.vel_y, rects_colision)