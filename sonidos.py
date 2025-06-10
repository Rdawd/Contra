import pygame
import sys
import os
def recurso(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return ruta_relativa


pygame.mixer.init()

def inicio_sonido():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//pantalla_de_inicio//retro-synth-loop-128-41048.mp3"))
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)
    
def cursor():
    sonido_cursor = pygame.mixer.Sound(recurso("Recursos//Sonidos//pantalla_de_inicio//1or2players//arcade-ui-18-229517.mp3"))
    sonido_cursor.set_volume(0.5)
    sonido_cursor.play()
    
def tema_nvl():
    pygame.mixer.music.load(recurso("Recursos//Sonidos//tema_primer_stage//game-over-groove-306764.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
def explocion():
    sonido_explosion = pygame.mixer.Sound(recurso("Recursos//Sonidos//death_personajes//8-bit-explosion-95847.mp3"))
    sonido_explosion.set_volume(0.5)
    sonido_explosion.play()
    
def balas():
    sonido_balas = pygame.mixer.Sound(recurso("Recursos//Sonidos//shoot//shoot-6-81136.mp3"))
    sonido_balas.set_volume(0.5)
    sonido_balas.play()