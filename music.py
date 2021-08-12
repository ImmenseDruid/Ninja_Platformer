import pygame
import os

pygame.mixer.pre_init(44100, -16, 64, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

jumpSound = pygame.mixer.Sound(os.path.join('SFX', 'jump.wav'))
pickUpSound = pygame.mixer.Sound(os.path.join('SFX','coinPickup.wav'))
hitSound = pygame.mixer.Sound(os.path.join('SFX','hitSound.wav'))
turretSound = pygame.mixer.Sound(os.path.join('SFX','gunShoot.wav'))
explosionSound = pygame.mixer.Sound(os.path.join('SFX','explosion.wav'))

sfxChannel =  pygame.mixer.Channel(0)

def play(soundObject):
	
	pygame.mixer.find_channel().play(soundObject)

def setSFXVolume(vol):
	for i in range(63):
		pygame.mixer.Channel(i).set_volume(vol)
