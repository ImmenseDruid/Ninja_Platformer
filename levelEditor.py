import pygame
import pickle
import os
import ui
import engine

from pygame.locals import *

pygame.font.init()

font = pygame.font.SysFont("Courier New", 10)


def load():
	with open(os.path.join('Levels', f'level{level}_data.p'), 'rb') as file:
		data = pickle.load(file)
		tiles.clear()
		for row in data:
			tiles.append(row)

def createNewLevel():
	tiles.clear()
	for y in range(levelHeight):
		tiles.append([])
		for x in range(levelWidth):
			tiles[y].append([x * tile_size[0], y * tile_size[1], -1])


	save()


def save():
	with open(os.path.join('Levels', f'level{level}_data.p'), 'wb') as file:
		pickle.dump(tiles, file)

brush = [0, 0]
levelHeight = 20
levelWidth = 20
tile_size = (32, 32)
screen_size = ((levelWidth * tile_size[0] + 200, levelHeight * tile_size[1]))
panel_size = (200, screen_size[1])
panel_pos = (screen_size[0] - panel_size[0], 0)
panel = ui.Panel(panel_pos[0], panel_pos[1], pygame.Surface(panel_size))
tiles = []
objects = []
screen = pygame.display.set_mode(screen_size)

level = 0

found = False
for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
	if f'level{level}_data.p' in files:
		found = True
if found:
	load()
else:
	createNewLevel()

b_save = ui.Button(20, 20, (50, 30), img = font.render("Save", False, (255, 255, 255)))
b_load = ui.Button(20, 70, (50, 30), img = font.render("Load", False, (255, 255, 255)))

#Buttons for Each Tile

b_T_BG = ui.Button(90, 20, (20, 20), engine.Tile.C_BG)
b_T_Ground = ui.Button(90, 60, (20, 20), engine.Tile.C_Ground, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'Ground.png')), (20, 20)))
b_T_Wall = ui.Button(90, 100, (20, 20), engine.Tile.C_Wall, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'Wall.png')), (20, 20)))

b_T_Spikes = ui.Button(90, 140, (20, 20), engine.Tile.C_Spikes, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'spikes.png')).convert_alpha(), (20, 20)))
b_T_Lava = ui.Button(90, 180, (20, 20), engine.Tile.C_Lava, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'lava.png')).convert_alpha(), (20, 20)))
b_T_Enemy_Basic = ui.Button(90, 220, (20, 20), engine.Tile.C_Enemy_Basic, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'groundEnemy.png')).convert_alpha(), (20, 20)))
b_T_Enemy_Flying = ui.Button(90, 260, (20, 20), engine.Tile.C_Enemy_Flying, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'flyingEnemy.png')).convert_alpha(), (20, 20)))
b_T_Enemy_Turret = ui.Button(90, 300, (20, 20), engine.Tile.C_Enemy_Turret, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'turretBase.png')).convert_alpha(), (20, 20)))
b_T_Enemy_Rocket_Turret = ui.Button(90, 340, (20, 20), engine.Tile.C_Enemy_Rocket_Turret, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'turretBase.png')).convert_alpha(), (20, 20)))

b_T_PlayerSpawn = ui.Button(130, 20, (20, 20), engine.Tile.C_PlayerSpawn)
b_T_PlayerGoal = ui.Button(130, 60, (20, 20), engine.Tile.C_PlayerGoal, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'flag.png')).convert_alpha(), (20, 20)))
b_T_Coin =  ui.Button(130, 100, (20, 20), engine.Tile.C_Coin, pygame.transform.scale(pygame.image.load(os.path.join('Images', 'coin.png')).convert_alpha(), (20, 20)))
b_T_Key = ui.Button(130, 140, (20, 20), engine.Tile.C_Key)




run = True
clicked = False
action = False
while run:
	screen.fill((0,0,0))

	for event in pygame.event.get():
		if event.type == QUIT:
			run = False

		if event.type == KEYDOWN:
			if event.key == K_UP:
				level += 1
				found = False
				for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
					if f'level{level}_data.p' in files:
						found = True
				if found:
					load()
				else:
					createNewLevel()

			if event.key == K_DOWN:
				level -= 1
				level = max(0, level)
				load()


	pygame.draw.rect(panel.surface, (0, 100, 100), pygame.Rect((0, 0), panel_size))
	
	if b_save.draw(panel):
		print('saves')
		save()
	if b_load.draw(panel):
		import game
		game.main(level)
		screen = pygame.display.set_mode(screen_size)



	if b_T_BG.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_BG
	if b_T_Ground.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Ground
	if b_T_Wall.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Wall
	if b_T_Spikes.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Spikes
	if b_T_Lava.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Lava

	if b_T_Enemy_Basic.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Enemy_Basic

	if b_T_Enemy_Flying.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Enemy_Flying

	if b_T_Enemy_Turret.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Enemy_Turret
	if b_T_Enemy_Rocket_Turret.draw(panel):
		brush[0] = 0
		brush[1] = engine.Tile.T_Enemy_Rocket_Turret

	if b_T_PlayerSpawn.draw(panel):
		brush[1] = engine.Tile.T_PlayerSpawn
	if b_T_PlayerGoal.draw(panel):
		brush[1] = engine.Tile.T_PlayerGoal
	if b_T_Coin.draw(panel):
		brush[1] = engine.Tile.T_Coin
	if b_T_Key.draw(panel):
		brush[1] = engine.Tile.T_Key

	tilePos = [pygame.mouse.get_pos()[0] // tile_size[0], pygame.mouse.get_pos()[1] // tile_size[1]]

	if pygame.mouse.get_pressed()[0] == 1:
			if tilePos[0] < panel_pos[0] // tile_size[0]:
				tiles[tilePos[1]][tilePos[0]][2] = brush[1]
			


	for row in tiles:
		for tile in row:
			pygame.draw.rect(screen, engine.Tile.colorDict[tile[2]], pygame.Rect((tile[0], tile[1]), tile_size))


	screen.blit(panel.surface, panel_pos)

	pygame.display.update()
