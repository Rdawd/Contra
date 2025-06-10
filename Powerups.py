import pygame

class PowerUp:
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        # Atributos físicos
        self.vel_y = 0            
        self.gravity = 0.5        
        self.rebound_factor = 0.8 # Factor de rebote (la energía que conserva al rebotar)

    def update(self, rects_collision):
        # Actualiza la animación
        cooldown_animacion = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        
        # Aplicamos la gravedad: aumenta la velocidad y actualiza la posición vertical.
        self.vel_y += self.gravity
        self.shape.y += self.vel_y

        # Verificamos colisiones contra cada rectángulo de colisión 
        for rect in rects_collision:
            if self.shape.colliderect(rect):
                # Si esta cayendo rebota poquito
                if self.vel_y > 0:
                    # Ajustamos la posición para que el power up se posicione justo encima del rectángulo
                    self.shape.bottom = rect.top
                    # Aplicamos el rebote, invirtiendo la velocidad 
                    self.vel_y = -self.vel_y * self.rebound_factor

    def draw(self, screen, scroll_x):
        # Al dibujar restamos el scroll para que se mantenga en su posición en el mundo
        imagen_actual = pygame.transform.flip(self.image, True, False)
        draw_rect = self.shape.copy()
        draw_rect.x -= scroll_x
        screen.blit(imagen_actual, draw_rect)
        screen.blit(self.image, (self.shape.x - scroll_x, self.shape.y))