import pygame


pygame.font.init()

class Panel():
	def __init__(self, x, y, surface):
		self.x = x
		self.y = y
		self.surface = surface


class Label():
	def __init__(self, x, y, text, font = "Times New Roman", size = 16):
		self.x = x 
		self.y = y 
		self.text = text
		self.fontName = font
		self.size = size

	def draw(self, screen):
		font =  pygame.font.SysFont(self.fontName, self.size)

		img = font.render(self.text, False, (255, 255, 255))

		screen.surface.blit(img, (self.x + screen.x, self.y + screen.y))


class Slider():

	HOVER_COL = (200, 200, 200)
	REGULAR_COL = (100, 100, 100)

	def __init__(self, x, y, size):
		self.x = x
		self.y = y

		self.p = 0
		self.min = 0
		self.max = 1

		self.width = size[0]
		self.height = size[1]

		self.clicked = False

	def draw(self, screen):
		rect = pygame.Rect(self.x + self.p * self.width + screen.x, self.y + screen.y, self.width // 5, self.height)
		pos = pygame.mouse.get_pos()

		color = self.REGULAR_COL

		if rect.collidepoint(pos):			

			color = self.HOVER_COL

			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = True

			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				self.clicked = False

		if self.clicked:
			self.p = (pos[0] - self.x - screen.x - (self.width // 10)) / self.width 

			self.p = min(self.p, self.max)
			self.p = max(self.p, self.min)


		surf = pygame.Surface((self.width + self.width // 5, self.height))
		pygame.draw.rect(surf, (50, 50, 50), pygame.Rect(5, 2 * self.height // 5, self.width, self.height // 5))
		pygame.draw.rect(surf, color, pygame.Rect((self.p * self.width, 0), (self.width // 5, self.height)))

		screen.surface.blit(surf, (self.x + screen.x, self.y + screen.y))

		return self.p

class Button():

	HOVER_COL = (200, 200, 200)
	CLICKED_COL = (0, 0, 0)
	ACTION_COL = (255, 255, 255)


	def __init__(self, x, y, size, color = (0, 100, 0), img = None):

		self.x = x
		self.y = y

		
		self.color = color

		self.clicked = False

		if img:
			self.img = img
			imgSize = [img.get_rect().w, img.get_rect().h]
			if size[0] > img.get_rect().w:
				imgSize[0] = size[0]
			else:
				imgSize[0] = img.get_rect().w + 10

			if size[1] > img.get_rect().h:
				imgSize[1] = size[1]
			else:
				imgSize[1] = img.get_rect().h + 10


			self.size = (imgSize[0], imgSize[1])
			surf = pygame.Surface(self.size)
			pygame.draw.rect(surf, color, pygame.Rect((0, 0), self.size))
		else:
			surf = pygame.Surface((size[0], size[1]))
			pygame.draw.rect(surf, color, pygame.Rect((0, 0), (size)))
			self.img = surf
			self.size = size

	def set_pos(self, x, y):
		self.x = x 
		self.y = y 


	def draw(self, screen):
		rect = pygame.Rect((self.x + screen.x, self.y + screen.y), self.size)
		pos = pygame.mouse.get_pos()

		
		col = self.color


		action = False

		if rect.collidepoint(pos):

			if pygame.mouse.get_pressed()[0] == 1:
				self.clicked = True
				col = self.CLICKED_COL
				
				
 
			if pygame.mouse.get_pressed()[0] == 0 and not self.clicked:
				col = self.HOVER_COL
				


			if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
				action = True
				self.clicked = False
				col = self.ACTION_COL
				


		#Create Border
		surf = pygame.Surface((self.size[0] + 4, self.size[1] + 4))
		pygame.draw.rect(surf, col, pygame.Rect(0, 0, self.size[0] + 4, self.size[1] + 4))

		#Blit image to button
		surf.blit(self.img, (2 + self.size[0] // 2 - self.img.get_rect().w // 2 , 2 + self.size[1] // 2 - self.img.get_rect().h // 2))


		screen.surface.blit(surf, (self.x, self.y))
		return action
