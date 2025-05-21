
import pygame


class Personaje():
    def __init__(self, x, y, animaciones_sin_apuntar):
        
        # Variable flip o voltear en false para que el jugador no se voltee
        self.flip = False
        
        self.animaciones = animaciones_sin_apuntar
        # imagen de la animacion que se esta mostrando actualmente o sea la inicial, haciendo que siempre regrese a la inicial
        self.frame_index = 0
        
        # Se almacena la hora en milisegundos desde que se inicia para poder controlar la velocidad de las imagenes 
        self.update_time = pygame.time.get_ticks()
        
        # determinas el shape o la forma que vas a crear, (coordenada, coordenada, tamaño, tamaño) de aqui saco x y 
        self.image = self.animaciones[self.frame_index]
        self.shape = pygame.Rect(0, 0, 20, 20)
        self.shape.center = (x,y)
        
        
        # recorre frame index en 0 sumandole 1 hasta completar el array animaciones_sin_apuntar, el segundo if lo vuelve a igualar a cero para que no de error
    def update(self):
        cooldown_aniamacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_aniamacion:
            self.frame_index = (self.frame_index + 1) 
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
        
        
    def draw(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image,self.flip,flip_y= False)
        # blit te permite dibujar las imagenes en pantalla
        interfaz.blit(imagen_flip,self.shape)
        
    # Esta linea la usaremos para ver las colisiones del personaje cuando esten las plataformas 
        # pygame.draw.rect(interfaz, (255, 255, 0), self.shape, width=1)
        
        
    def movimiento(self, delta_x, delta_y):
        
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y