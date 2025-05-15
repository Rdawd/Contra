import pygame

class Weapon():
    def __init__(self, imagenes_arma):
        self.animaciones = imagenes_arma  # Lista recibida desde fuera
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        
        # Imagen inicial
        self.image = self.animaciones[0]
        self.shape = self.image.get_rect()

    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.shape)

    def update(self, jugador):
        # Actualiza la animación del arma
        cooldown_aniamacion = 150

        if pygame.time.get_ticks() - self.update_time >= cooldown_aniamacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()

        # Frame actual
        self.image = self.animaciones[self.frame_index]

        
        self.flip = jugador.flip

        # Aplica el flip si es necesario
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

        # Posición centrada en el jugador
        self.shape.centerx = jugador.shape.centerx
        self.shape.centery = jugador.shape.centery

    # Ya no necesitas esta función a menos que la uses para algo más
    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x += delta_x
        self.shape.y += delta_y
