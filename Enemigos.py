import pygame

class Enemigo:
    def __init__(self, x, y, animaciones):
        self.alive = True
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = True

        self.image = self.animaciones[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        
    def update(self):
        cooldown_animacion = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        
    def draw(self, screen):
        imagen_actual = pygame.transform.flip(self.image, False,False) 
        
        screen.blit(imagen_actual, self.shape)
        pygame.draw.rect(screen, (255, 255, 0), self.shape, width=1)
    def movimiento(self, delta_x, delta_y):
        self.shape.x += delta_x
        self.shape.y += delta_y

    def perseguir(self, objetivo):
        if self.shape.x < objetivo.shape.x:
            self.movimiento(1, 0)
        elif self.shape.x > objetivo.shape.x:
            self.movimiento(-1, 0)

