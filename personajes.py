import pygame

class Personaje:
    def __init__(self, x, y, animaciones_sin_apuntar, weapons_dict=None, animaciones_saltando=None):
        self.flip = True
        self.animaciones = animaciones_sin_apuntar
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        self.shape = pygame.Rect(0, 0, 20, 20)
        self.shape.center = (x, y)

        # Atributos de movimiento y estado
        self.vel_y = 0
        self.en_suelo = False
        self.alive = True
        self.world_x = x
        self.world_y = y
        self.vida = 5
        self.vida_maxima = 5

        # Sistema de armas/apuntado
        self.weapons = weapons_dict if weapons_dict is not None else {}
        self.current_weapon = self.weapons.get("nada", None)
        self.apuntando = False

        # Salto
        self.saltando = False
        self.animaciones_saltando = animaciones_saltando if animaciones_saltando is not None else []
        self.frame_index_salto = 0
        self.salto_update_time = pygame.time.get_ticks()

        # Coyote time
        self.COYOTE_TIME_MAX = 150  # milisegundos
        self.coyote_timer = 0

        # Sistema de disparo y cargador
        self.tipo_disparo = "bala_1"  
        self.ammo_max = 10           # Capacidad del cargador
        self.ammo_actual = self.ammo_max
        self.reload_time = 2000      # Tiempo de recarga en milisegundos 
        self.reloading = False
        self.last_reload_time = 0
        
        self.fire_rate = 300         # Tiempo mínimo entre disparos en milisegundos
        self.last_shot_time = 0 

    def set_apuntado(self, apuntando, direccion="nada"):
        # Si está saltando y no está en el suelo, no permitimos cambiar la animación de apuntado
        if self.saltando and not self.en_suelo:
            return

        # Corrige la dirección para que se ajuste a los nombres de las armas
        direccion_corregida = direccion.lower().replace(" ", "_")
        
        if self.apuntando != apuntando or (apuntando and self.current_weapon != self.weapons.get(direccion_corregida)):
            if apuntando and (direccion_corregida in self.weapons):
                self.current_weapon = self.weapons[direccion_corregida]
            else:
                self.current_weapon = self.weapons.get("nada", None)
            if self.current_weapon:
                self.current_weapon.frame_index = 0
                self.current_weapon.update_time = pygame.time.get_ticks()
        self.apuntando = apuntando

    def update(self):
        now = pygame.time.get_ticks()

        # Animación de salto
        if self.saltando and self.animaciones_saltando:
            cooldown_salto = 100
            if now - self.salto_update_time >= cooldown_salto:
                self.frame_index_salto = (self.frame_index_salto + 1) % len(self.animaciones_saltando)
                self.salto_update_time = now
            self.image = self.animaciones_saltando[self.frame_index_salto]
        else:
            cooldown = 100
            if now - self.update_time >= cooldown:
                self.frame_index = (self.frame_index + 1) % len(self.animaciones)
                self.update_time = now
            self.image = self.animaciones[self.frame_index]

        # esto permite que la animación del disparo se ejecute
        if self.apuntando and self.current_weapon:
            self.current_weapon.update(self)

        # Coyote time
        if not self.en_suelo:
            tiempo_pasado = now - self.update_time
            self.coyote_timer -= tiempo_pasado
            self.coyote_timer = max(0, self.coyote_timer)
        else:
            self.coyote_timer = self.COYOTE_TIME_MAX

        #  Actualización del sistema de recarga:
        if self.reloading:
            if now - self.last_reload_time >= self.reload_time:
                self.ammo_actual = self.ammo_max
                self.reloading = False
                

    def draw(self, interfaz, scroll_x=0):
        rect_dibujo = self.shape.copy()
        rect_dibujo.x = self.world_x - scroll_x
        rect_dibujo.y = self.world_y
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)

        if self.saltando:
            interfaz.blit(imagen_flip, rect_dibujo)
        else:
            if self.apuntando and self.current_weapon:
                self.current_weapon.dibujar(interfaz)
            else:
                interfaz.blit(imagen_flip, rect_dibujo)

    def movimiento(self, delta_x, delta_y, rects_colision):
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        # Reinicia el estado de suelo
        self.en_suelo = False

        # Movimiento horizontal
        self.world_x += delta_x
        self.shape.x = self.world_x
        for rect in rects_colision:
            if self.shape.colliderect(rect):
                if delta_x > 0:
                    self.shape.right = rect.left
                    self.world_x = self.shape.x
                elif delta_x < 0:
                    self.shape.left = rect.right
                    self.world_x = self.shape.x

        # Movimiento vertical
        self.world_y += delta_y
        self.shape.y = self.world_y
        for rect in rects_colision:
            if self.shape.colliderect(rect):
                if delta_y > 0:
                    self.shape.bottom = rect.top
                    self.vel_y = 0
                    self.world_y = self.shape.y
                    self.en_suelo = True
                    self.saltando = False
                elif delta_y < 0:
                    self.shape.top = rect.bottom
                    self.vel_y = 0
                    self.world_y = self.shape.y

    def draw_con_offset(self, screen, pos_x, pos_y):
        
        screen.blit(self.image, (pos_x, pos_y))
        
    def movimiento_sin_colisiones(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.world_x += delta_x
        self.world_y += delta_y
        self.shape.x = self.world_x
        self.shape.y = self.world_y