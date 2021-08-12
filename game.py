import pygame
import pickle
import engine
import ui, os, music
from os import path
from pygame.locals import *


music_volume = 0.25
sfx_volume = 0.25

pygame.font.init()
font = pygame.font.SysFont("Courier New", 16)

pygame.mixer.music.load('music16.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(music_volume)

times = []
coins = []
max_coins = []


for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
		for file in files:
			times.append(0)
			coins.append(0)
			max_coins.append(0)


if not os.path.isfile('high_scores.pickle'):
	with open('high_scores.pickle', 'wb') as file:	
		pickle.dump([times, coins, max_coins], file)

if not os.path.isfile('settings.pickle'):
	with open('settings.pickle', 'wb') as file:
				pickle.dump([sfx_volume, music_volume], file)
#with open('high_scores.json', 'w') as file:	
#	json.dump([times, coins, max_coins], file)

def main(start_level):
	
	pygame.init()
	

	pygame.mixer.music.load('music16.wav')

	pygame.mixer.music.play(-1)
	global music_volume, sfx_volume
	pygame.mixer.music.set_volume(music_volume)

	music.setSFXVolume(sfx_volume)

	backgroundColor = (20, 20, 20)

	level = engine.Level()
	level.current_level = start_level

	level_size = (20, 20)
	tile_size = (32, 32)
	screen_size = (level_size[0] * tile_size[0], level_size[1] * tile_size[1])
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption('Platformer')


	clock = pygame.time.Clock()
	timer = 0
	level.load(level.current_level)

	
	run = True
	while run:
		delta = clock.tick(60)
		timer += delta
		screen.fill(backgroundColor)

		timer_label = ui.Label(10, 20, f'{timer / 1000}')
		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
				#pygame.quit()
				#quit()

			if event.type == KEYDOWN:
				if event.key == K_a:
					level.playerRef.movingLeft = True
				if event.key == K_d:
					level.playerRef.movingRight = True
				if event.key == K_w:
					level.playerRef.jump = True	
				if event.key == K_ESCAPE:
					game_settings()
					screen = pygame.display.set_mode(screen_size)

			if event.type == KEYUP:
				if event.key == K_a:
					level.playerRef.movingLeft = False
				if event.key == K_d:
					level.playerRef.movingRight = False

		if level.playerRef.alive:
			pass
		else:
			level.load(level.current_level)

		

		for tile in level.tiles:
			tile.render(screen)

		for i, entity in reversed(list(enumerate(level.entities))):
			
			if not entity.alive: 
				level.entities.pop(i)

			if entity.update():
				#This is such a BAD way of doing this
				global times, max_coins, coins
				if timer < times[level.current_level] or times[level.current_level] == 0:
					times[level.current_level] = timer
				max_coins[level.current_level] = level.coins
				coins[level.current_level] = level.playerRef.coins
				level.playerRef.coins = 0
				timer = 0
				level.current_level += 1
				with open('high_scores.pickle', 'wb') as file:	
					pickle.dump([times, coins, max_coins], file)


				


				level.load(level.current_level)
			entity.render(screen)

		timer_label.draw(ui.Panel(0,0, screen))


		pygame.display.update()

	#pygame.quit()
	#quit()


def settings():
	pygame.init()

	start_menu_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'MainScreenBackground.png'))).convert_alpha()

	screen = pygame.display.set_mode((500, 500))
	main_panel = ui.Panel(0, 0, screen)
	slider_panel = ui.Panel(200, 100, screen)

	clock = pygame.time.Clock()

	run = True

	menu_button = ui.Button(20, 100, (150, 50), (0, 100, 100), font.render("Main Menu", False, (255, 255, 255)))
	apply_button = ui.Button(20, 160, (150, 50), img = font.render("Save Settings", False, (255, 255, 255)))
	music_volume_slider = ui.Slider(100, 0, (100, 20))
	sfx_volume_slider = ui.Slider(100, 50, (100, 20))
	music_volume_label = ui.Label(0, 0, 'Music Volume')
	sfx_volume_label = ui.Label(0, 50, 'SFX Volume')
	global music_volume, sfx_volume
	music_volume_slider.p = music_volume
	sfx_volume_slider.p = sfx_volume

	while run:

		clock.tick(30)
		screen.blit(start_menu_BG, (0, 0))

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
				

		if menu_button.draw(main_panel):
			start_menu()

		if apply_button.draw(main_panel):
			#save stuff in pickle
			with open('settings.pickle', 'wb') as file:
				pickle.dump([sfx_volume, music_volume], file)
			


		music_volume_label.draw(slider_panel)
		sfx_volume_label.draw(slider_panel)

		music_temp = music_volume_slider.draw(slider_panel)
		if music_volume != music_temp:
			music_volume = music_temp
			pygame.mixer.music.set_volume(music_volume)

		sfx_temp = sfx_volume_slider.draw(slider_panel)
		if sfx_temp != sfx_volume:
			sfx_volume = sfx_temp
			music.setSFXVolume(sfx_volume)
			music.play(music.pickUpSound)

		pygame.display.update()


	pygame.quit()
	quit()

def game_settings():
	pygame.init()

	start_menu_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'MainScreenBackground.png'))).convert_alpha()

	screen = pygame.display.set_mode((500, 500))
	main_panel = ui.Panel(0, 0, screen)
	slider_panel = ui.Panel(200, 100, screen)

	clock = pygame.time.Clock()

	run = True

	menu_button = ui.Button(20, 100, (150, 50), (0, 100, 100), font.render("Main Menu", False, (255, 255, 255)))
	apply_button = ui.Button(20, 160, (150, 50), img = font.render("Save Settings", False, (255, 255, 255)))
	return_button = ui.Button(20, 220, (150, 50), (0, 100, 100), font.render("Return", False, (255, 255, 255)))
	music_volume_slider = ui.Slider(100, 0, (100, 20))
	sfx_volume_slider = ui.Slider(100, 50, (100, 20))
	music_volume_label = ui.Label(0, 0, 'Music Volume')
	sfx_volume_label = ui.Label(0, 50, 'SFX Volume')
	global music_volume, sfx_volume
	music_volume_slider.p = music_volume
	sfx_volume_slider.p = sfx_volume

	while run:

		clock.tick(30)
		screen.blit(start_menu_BG, (0, 0))

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		if menu_button.draw(main_panel):
			start_menu()

		if apply_button.draw(main_panel):
			#save stuff in pickle
			with open('settings.pickle', 'wb') as file:
				pickle.dump([sfx_volume, music_volume], file)
			
		if return_button.draw(main_panel):
			return

		music_volume_label.draw(slider_panel)
		sfx_volume_label.draw(slider_panel)

		music_temp = music_volume_slider.draw(slider_panel)
		if music_volume != music_temp:
			music_volume = music_temp
			pygame.mixer.music.set_volume(music_volume)

		sfx_temp = sfx_volume_slider.draw(slider_panel)
		if sfx_temp != sfx_volume:
			sfx_volume = sfx_temp
			music.setSFXVolume(sfx_volume)
			music.play(music.pickUpSound)

		pygame.display.update()


	pygame.quit()
	quit()

def level_select():
	pygame.init()

	run = True
	screen = pygame.display.set_mode((500, 500))
	start_menu_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'MainScreenBackground.png'))).convert_alpha()

	panel = ui.Panel(50, 50, pygame.Surface((screen.get_width() - 50, screen.get_height() - 50)))
	panel.surface.set_colorkey((0,0,0))



	spacing = 80
	real_width = screen.get_width() - 50 - 50
	xMax = real_width / (spacing)



	buttons = []
	labels = []


	start_menu_button = ui.Button(0, 350, (150, 50), img = font.render('Main Menu', False, (255, 255, 255)))

	level = 0
	for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
		y = 0
		for file in files:
			x = ((level) % (xMax)) * spacing
			y = (level // xMax) * spacing
			buttons.append(ui.Button(x,  y, (50, 50), img = font.render(f'{level + 1}', False, (255, 255, 255))))
			labels.append(ui.Label(x - 50, y, f'{times[level] / 1000}'))
			labels.append(ui.Label(x - 50, y + 10, f'{coins[level]} / {max_coins[level]}'))
			level += 1

	#level = 0
	#print(len(buttons))
	for i, c in enumerate(coins):
			print(f'{c} / {max_coins[i]}')


	while run:
		screen.blit(start_menu_BG, (0, 0))

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False

		for i, button in enumerate(buttons):
			

			#button.set_pos()
			#button.x = (i * 80) % (screen.get_width() - 100)
			#button.y = (i * 80) / (screen.get_width() - 100)

			if button.draw(panel):
				main(i)
				screen = pygame.display.set_mode((500, 500))

		for label in labels:
			label.draw(panel)

		
		if start_menu_button.draw(panel):
			run = False



		screen.blit(panel.surface, (panel.x, panel.y))
		pygame.display.update()







def start_menu():
	pygame.init()
	
	with open('settings.pickle', 'rb') as file:
		settings_options = pickle.load(file)

	with open('high_scores.pickle', 'rb') as file:
		high_scores = pickle.load(file)

	#with open('high_scores.json', 'r') as file:
	#	high_scores = json.load(file)

	sfx_volume = settings_options[0]
	music_volume = settings_options[1]
	global times, coins, max_coins
	times = high_scores[0]
	coins = high_scores[1]
	max_coins = high_scores[2]


	

	screen = pygame.display.set_mode((500, 500))
	start_menu_BG = pygame.transform.scale2x(pygame.image.load(os.path.join('Images', 'MainScreenBackground.png'))).convert_alpha()
	panel = ui.Panel(50, 0, pygame.Surface((screen.get_width() - 50, screen.get_height())))
	panel.surface.set_colorkey((0,0,0))
	run = True

	play_button = ui.Button(0, 100, (150, 50), img = font.render("Play", False, (255, 255, 255)))
	settings_button = ui.Button(0, 160, (150, 50), img = font.render("Settings", False, (255, 255, 255)))
	level_select_button = ui.Button(0, 220, (150, 50), img = font.render("Level Select", False, (255, 255, 255)))
	quit_button = ui.Button(0, 280, (150, 50), img = font.render("Quit", False, (255, 255, 255)))
	clock = pygame.time.Clock()


	while run:

		clock.tick(30)
		screen.blit(start_menu_BG, (0, 0))

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					run = False
					

		if play_button.draw(panel):
			main(0)
			screen = pygame.display.set_mode((500, 500))

		if settings_button.draw(panel):
			settings()

		if level_select_button.draw(panel):
			level_select()
			screen = pygame.display.set_mode((500, 500))


		if quit_button.draw(panel):
			run = False


		screen.blit(panel.surface, (panel.x, panel.y))

		pygame.display.update()

	with open('high_scores.pickle', 'wb') as file:
		pickle.dump([times, coins, max_coins], file)
	pygame.quit()
	quit()

if __name__ == '__main__':
	start_menu()