import pygame
import music
import pickle, os
import math

tileSize = (32, 32)



def sign(x):
	return x / abs(x) if x != 0 else 1


def raycast2D(start, angle, maxDist):
	dist = 0
	xOffset = start[0]
	yOffset = start[1]
	result = start
	while dist < maxDist:
		dist += 1



class Level():
	def __init__(self, entities = [], tiles = []):
		self.entities = entities
		self.tiles = tiles
		self.playerRef = None
		self.current_level = 0
		self.coins = 0

	def loadLevel(self, level):
		with open(os.path.join('Levels', f'level{level}_data.p'), 'rb') as file:
			data = pickle.load(file)
			self.tiles.clear()
			self.entities.clear()
			self.coins = 0
			for row in data:
				for tile in row:
					if tile[2] == Tile.T_BG:
						pass
					if tile[2] == Tile.T_Ground:
						self.tiles.append(Tile(tile[0], tile[1], tile[2]))
					if tile[2] == Tile.T_Wall:
						self.tiles.append(Tile(tile[0], tile[1], tile[2]))
					if tile[2] == Tile.T_Spikes:
						#self.tiles.append(Tile(tile[0], tile[1], tile[2]))
						self.entities.append(Spike(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'spikes.png')).convert_alpha()))
					if tile[2] == Tile.T_PlayerGoal:
						#tiles.append(engine.Tile(tile[0], tile[1], tile[2]))
						self.entities.append(NextLevelFlag(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'flag.png')).convert_alpha()))
					if tile[2] == Tile.T_PlayerSpawn:
						#tiles.append(engine.Tile(tile[0], tile[1], tile[2]))
						self.playerRef = Player(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'player.png')).convert_alpha())
						self.entities.append(self.playerRef)
					if tile[2] == Tile.T_Coin:
						self.coins += 1
						self.entities.append(Coin(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'coin.png')).convert_alpha()))
					if tile[2] == Tile.T_Key:
						self.entities.append(Key(tile[0], tile[1]))
					if tile[2] == Tile.T_Lava:
						self.entities.append(Lava(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'lava.png')).convert_alpha()))

					if tile[2] == Tile.T_Enemy_Flying:
						self.entities.append(Enemy_Flying(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'flyingEnemy.png')).convert_alpha()))

					if tile[2] == Tile.T_Enemy_Basic:
						self.entities.append(Enemy(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'groundEnemy.png')).convert_alpha()))

					if tile[2] == Tile.T_Enemy_Turret:
						self.entities.append(Enemy_Turret(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'turretBase.png')).convert_alpha()))

					if tile[2] == Tile.T_Enemy_Rocket_Turret:
						self.entities.append(Enemy_Rocket_Turret(tile[0], tile[1], pygame.image.load(os.path.join('Images', 'turretBase.png')).convert_alpha()))

			for e in self.entities:
				e.tiles = self.tiles
				#global player
				e.player = self.playerRef

	def load(self, level):
		found = False
		for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'Levels')):
			if f'level{level}_data.p' in files:
				found = True
		if found:
			self.loadLevel(level)
		else:
			
			self.current_level = 0
			self.loadLevel(self.current_level)

	def loadGameOverScene(self):
		pass

	def loadMainMenu(self):
		pass



class Entity():
	def __init__(self, x, y, img, enabled = True):
		self.rect = pygame.Rect((x, y), img.get_rect().size)
		#self.rect.x = self.rect.centerx
		#self.rect.y = self.rect.centery

		self.img = img
		self.img.set_colorkey((0, 0, 0))

		self.v = [0, 0]
		self.a = [0, .2]
		self.forces = []

		self.tiles = []
		self.player = None

		self.alive = True
		self.enabled = enabled

	
	def render(self, screen):
		screen.blit(self.img, (self.rect.x, self.rect.y))

	def update(self):
		if self.enabled:
			if self.alive:
				self.v[0] += self.a[0]
				self.v[1] += self.a[1]

				dx = self.v[0]
				dy = self.v[1]

				dx, dy = self.collide(dx, dy)
							

				self.v[0] = dx
				self.v[1] = dy

				self.rect.x += dx
				self.rect.y += dy

				if self.rect.y > 1000:
					self.alive = False


	def collideWithPlayer(self):
		if self is not self.player:
			return self.rect.colliderect(self.player.rect)
		else:
			return False

	def collide(self, dx, dy):
		for t in self.tiles:
			if t.rect.colliderect(pygame.Rect((self.rect.x + dx, self.rect.y), self.rect.size)):
				if self.v[0] < 0:
					dx = t.rect.x + t.rect.w - self.rect.x
				elif self.v[0] > 0:
					dx = t.rect.x - self.rect.w - self.rect.x


			if t.rect.colliderect(pygame.Rect((self.rect.x, self.rect.y + dy), self.rect.size)):
				if self.v[1] < 0:
					dy = t.rect.y + t.rect.h - self.rect.y
				elif self.v[1] > 0:
					dy = t.rect.y - self.rect.h - self.rect.y

		return dx, dy

class Character(Entity):
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((16, 16))
			pygame.draw.rect(img, (255, 0, 0), img.get_rect())

		self.movingLeft = False
		self.movingRight = False
		self.jump = False
		self.numJumps = 2
		self.canWallJump = False
		self.prev_jump = False

		self.speed = 5


		self.health = 1

		self.cyoteTime = 0
		self.cyoteTimer = 2

		super().__init__(x, y, img)

	def Jump(self):

		if self.canWallJump and self.jump :
			self.v[1] = -4
			music.play(music.jumpSound)
		elif self.numJumps > 0 and self.jump:
			self.numJumps -= 1
			self.v[1] = -8
			music.play(music.jumpSound)


		self.jump = False


	def collide(self, dx, dy):
		self.canWallJump = False
		for t in self.tiles:
			if t.rect.colliderect(pygame.Rect((self.rect.x + dx, self.rect.y), self.rect.size)):
				if self.v[0] < 0:
					dx = t.rect.x + t.rect.w - self.rect.x
					self.canWallJump = True
				elif self.v[0] > 0:
					dx = t.rect.x - self.rect.w - self.rect.x
					self.canWallJump = True


			if t.rect.colliderect(pygame.Rect((self.rect.x, self.rect.y + dy), self.rect.size)):
				if self.v[1] < 0:
					dy = t.rect.y + t.rect.h - self.rect.y
				elif self.v[1] > 0:
					dy = t.rect.y - self.rect.h - self.rect.y
					self.numJumps = 2

		return dx, dy


	def moveLeft(self):
		self.v[0] = -self.speed


	def moveRight(self):
		self.v[0] = self.speed

	def deadCheck(self):
		if self.health <= 0:
			self.alive = False

	def damage(self, amount):
		self.health -= amount
		music.play(music.hitSound)
		self.deadCheck()

	def render(self, screen):
		super().render(screen)

	def update(self):
		if self.enabled:
			if self.alive:

				if abs(self.v[0]) <= .1:
					self.v[0] = 0

				self.a[0] = - self.v[0] / 5

				

				if self.movingLeft:
					self.moveLeft()
				if self.movingRight:
					self.moveRight()
				if self.jump:
					self.Jump()

				if self.prev_jump and not self.jump and self.v[1] < 0:
					self.v[1] = 0
				self.prev_jump = self.jump
		
		super().update()

class Enemy(Character):
	def __init__(self, x, y, img = None):
		super().__init__(x, y, img)
		#self.speed = 3


	def update(self):
		if self.enabled:
			if self.alive:
				if self.player.rect.x < self.rect.x:
					self.moveLeft()
				elif self.player.rect.x > self.rect.x:
					self.moveRight()

				if self.player.rect.y < self.rect.y:
					self.Jump()


				if self.collideWithPlayer():
						self.player.damage(1)

				super().update()


	
				

class Enemy_Flying(Character):
	def __init__(self, x, y, img = None):
		
		super().__init__(x, y, img)
		self.a[1] = 0
		self.speed = 4

	def update(self):
		if self.enabled:
			if self.alive:
				if self.player.rect.x < self.rect.x - 5:
					self.moveLeft()
				elif self.player.rect.x > self.rect.x + 5:
					self.moveRight()

				if self.player.rect.y < self.rect.y:
					self.moveUp()
				if self.player.rect.y > self.rect.y:
					self.moveDown()

				if self.collideWithPlayer():
						self.player.damage(1)

				super().update()


		

	def moveDown(self):
		self.v[1] = self.speed // 2

	def moveUp(self):
		self.v[1] = -self.speed // 2

class Enemy_Turret(Character):

	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((32, 32))
			pygame.draw.rect(img, (255, 0, 0), img.get_rect())

		self.rotation = 0
		self.aw = 0
		self.ah = 0
		self.reloadResetTime = 100
		self.reloadTime = self.reloadResetTime
		self.bullets = []
		super().__init__(x, y, img)
		self.a = [0, 0]


	def shoot(self, w, h, mag):
		music.play(music.turretSound)
		self.reloadTime = self.reloadResetTime					
		self.bullets.append(Bullet(self.rect.centerx + 32 * w, self.rect.centery + 32 * h, [self.aw / mag, self.ah / mag]))
		self.bullets[len(self.bullets) - 1].player = self.player
		self.bullets[len(self.bullets) - 1].tiles = self.tiles


	def update(self):
		import math
		if self.enabled:
			if self.alive:
				if self.collideWithPlayer():
						self.player.damage(1)


				self.aw = self.player.rect.centerx - self.rect.centerx
				self.ah = self.player.rect.centery - self.rect.centery

				slope = abs(self.ah / self.aw) if self.aw != 0 else 100
				self.rotation = math.atan(slope)

				w = abs(math.cos(self.rotation))
				h = abs(math.sin(self.rotation))
				if self.aw < 0:
					w = -w
				if self.ah < 0:
					h = -h

				mag = math.sqrt((self.aw * self.aw) + (self.ah * self.ah))

				self.reloadTime -= 1
				if self.reloadTime < 0:
					self.shoot(w, h, mag)
					

				for i, bullet in reversed(list(enumerate(self.bullets))):
					if not bullet.alive:
						self.bullets.pop(i)
					bullet.update()


				
				#print(self.rotation * 90)

				super().update()

	def render(self, screen):
		import math
		super().render(screen)
		arm = pygame.Surface((32, 32))
		
		w = abs(math.cos(self.rotation))
		h = abs(math.sin(self.rotation))
		if self.aw < 0:
			w = -w
		if self.ah < 0:
			h = -h

		pygame.draw.line(screen, (0, 200, 0), (self.rect.center), (self.rect.centerx + 32 * w, self.rect.centery + 32 * h), 3)
		arm.set_colorkey((0, 0, 0))

		for bullet in self.bullets:
			bullet.render(screen)
		#screen.blit(pygame.transform.rotate(arm, self.rotation), (self.rect.x, self.rect.y))

class Enemy_Rocket_Turret(Character):
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((32, 32))
			pygame.draw.rect(img, (255, 0, 0), img.get_rect())

		self.rotation = 0
		self.aw = 0
		self.ah = 0
		self.reloadResetTime = 100
		self.reloadTime = self.reloadResetTime
		self.bullets = []
		super().__init__(x, y, img)
		self.a = [0, 0]

	def shoot(self, w, h, mag):
		self.reloadTime = self.reloadResetTime
		music.play(music.turretSound)
		self.bullets.append(Rocket(self.rect.centerx + 32 * w, self.rect.centery + 32 * h, [self.aw / mag, self.ah / mag]))
		self.bullets[len(self.bullets) - 1].player = self.player
		self.bullets[len(self.bullets) - 1].tiles = self.tiles


	def update(self):
		import math
		if self.enabled:
			if self.alive:
				if self.collideWithPlayer():
						self.player.damage(1)


				self.aw = self.player.rect.centerx - self.rect.centerx
				self.ah = self.player.rect.centery - self.rect.centery

				slope = abs(self.ah / self.aw) if self.aw != 0 else 100
				self.rotation = math.atan(slope)

				w = abs(math.cos(self.rotation))
				h = abs(math.sin(self.rotation))
				if self.aw < 0:
					w = -w
				if self.ah < 0:
					h = -h

				mag = math.sqrt((self.aw * self.aw) + (self.ah * self.ah))

				self.reloadTime -= 1
				if self.reloadTime < 0:
					self.shoot(w, h, mag)

				for i, bullet in reversed(list(enumerate(self.bullets))):
					if not bullet.alive:
						self.bullets.pop(i)
					bullet.update()


				
				#print(self.rotation * 90)

				super().update()

	def render(self, screen):
		import math
		super().render(screen)
		arm = pygame.Surface((32, 32))
		
		w = abs(math.cos(self.rotation))
		h = abs(math.sin(self.rotation))
		if self.aw < 0:
			w = -w
		if self.ah < 0:
			h = -h

		pygame.draw.line(screen, (0, 200, 0), (self.rect.center), (self.rect.centerx + 32 * w, self.rect.centery + 32 * h), 3)
		arm.set_colorkey((0, 0, 0))

		for bullet in self.bullets:
			bullet.render(screen)


class Player(Character):
	def __init__(self, x, y, img = None):
		self.coins = 0
		super().__init__(x, y, img)
	
class Object(Entity):
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((10, 10))
			pygame.draw.rect(img, (255, 0, 255), img.get_rect())

		super().__init__(x, y, img)

	def render(self, screen):
		super().render(screen)

	def collision_test(self, rect):
		return self.rect.colliderect(rect)

	def update(self):
		if self.enabled:
			if self.alive:
				pass


class Bullet(Object):
	def __init__(self, x, y, v, img = None):
		if not img:
			img = pygame.Surface((5, 5))
			pygame.draw.rect(img, (255, 255, 255), img.get_rect())



		super().__init__(x, y, img)

		self.lifeSpan = 500
		self.lifeTime = self.lifeSpan

		self.pos = [x, y]
		self.v = [v[0] * 5, v[1] * 5]
		self.a = [0, 0]



	def update(self):
		if self.enabled:
			if self.alive:
				self.lifeTime -= 1

				if self.lifeTime <= 0:
					self.alive = False


				self.pos[0] += self.v[0]
				self.pos[1] += self.v[1]

				self.rect.x = self.pos[0]
				self.rect.y = self.pos[1]

				self.collide()

				if self.collideWithPlayer():
					self.player.damage(1)

	def collide(self):
		for tile in self.tiles:
			if tile.rect.colliderect(self.rect):				
				self.alive = False

		#super().collide()

class Rocket(Object):	

	def __init__(self, x, y, v, img = None):
		if not img:
			#img = pygame.Surface((10, 10))
			#pygame.draw.rect(img, (255, 255, 255), img.get_rect())
			rocketImg = pygame.image.load(os.path.join('Images', 'Rocket.png')).convert_alpha()
			img = rocketImg

		super().__init__(x, y, img)

		self.lifeSpan = 500
		self.lifeTime = self.lifeSpan

		self.particleSys = ParticleSystem(x, y, 100, .1, [.2, None, [-self.v[0], -self.v[1]], [0, .1]])

		self.pos = [x, y]
		self.prevPos = self.pos
		self.v = [v[0] * 5, v[1] * 5]
		self.a = [0, 0]

		self.rotatedImg = img

	def update(self):
		if self.enabled:
			if self.alive:
				self.lifeTime -= 1

				if self.lifeTime <= 0:
					self.alive = False

				desiredDir = [self.player.rect.centerx - self.pos[0], self.player.rect.centery -  self.pos[1]]
				maxForce = 100
				self.a[0] = max(min((desiredDir[0] - self.v[0]), maxForce), -maxForce) / 10 
				self.a[1] = max(min((desiredDir[1] - self.v[1]), maxForce), -maxForce) / 10

				self.v[0] += self.a[0]
				self.v[1] += self.a[1]

				import math

				angle = math.atan2(self.v[0], self.v[1])
				#print(self.v)
				self.rotatedImg = pygame.transform.rotate(self.img, (angle - math.pi) * 180 / math.pi)
				self.rotatedImg.set_colorkey((0, 0, 0))
				
				v = math.sqrt(self.v[0] * self.v[0] + self.v[1] * self.v[1])

				self.prevPos = self.pos

				self.pos[0] += self.v[0] / v * 2
				self.pos[1] += self.v[1] / v * 2

				self.rect.x = self.pos[0]
				self.rect.y = self.pos[1]

				self.particleSys.pos = [self.prevPos[0] - self.v[0] / v * 6, self.prevPos[1] - self.v[1] / v * 6]
				self.particleSys.update()

				self.collide()

				if self.collideWithPlayer():
					self.player.damage(1)
					music.play(music.explosionSound)

	def render(self, screen):
		self.particleSys.render(screen)
		screen.blit(self.rotatedImg, (self.rect.x - self.rotatedImg.get_width() / 2, self.rect.y - self.rotatedImg.get_height() / 2))


	def collide(self):
		for tile in self.tiles:
			if tile.rect.colliderect(self.rect):
				music.play(music.explosionSound)				
				self.alive = False


class NextLevelFlag(Object):
	color = (10, 200, 0)
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((16, 16))
			pygame.draw.rect(img, (0, 0, 0), img.get_rect())
			pygame.draw.rect(img, self.color, pygame.Rect(2, 2, img.get_rect().w - 4, img.get_rect().h - 4))
		super().__init__(x, y, img)

	def render(self, screen):
		super().render(screen)

	def update(self):
		if self.enabled:
			if self.alive:
				if self.collideWithPlayer():
					return True


class Spike(Object):
	color = (255, 255, 255)
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((16, 16))
			pygame.draw.rect(img, self.color, img.get_rect())
		super().__init__(x, y, img)

	def render(self, screen):
		super().render(screen)

	def update(self):
		if self.enabled:
			if self.alive:
				if self.collideWithPlayer():
					self.player.damage(1)

class Lava(Object):
	color = (255, 0, 0)
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((16, 16))
			pygame.draw.rect(img, self.color, img.get_rect())
		super().__init__(x, y, img)

	def render(self, screen):
		super().render(screen)

	def update(self):
		if self.enabled:
			if self.alive:
				if self.collideWithPlayer():
					self.player.damage(1)
					#self.player.numJumps += 1
					#self.player.Jump()

class Coin(Object):
	color = (255, 200, 0)
	def __init__(self, x, y, img = None):
		if not img:
			img = pygame.Surface((16, 16))
			pygame.draw.rect(img, (0, 0, 0), img.get_rect())
			pygame.draw.rect(img, self.color, pygame.Rect(2, 2, img.get_rect().w - 4, img.get_rect().h - 4))
		self.move_counter = 0
		self.moveDirection = 1

		super().__init__(x, y, img)
		self.rect.x = self.rect.centerx
		self.rect.y = self.rect.centery

	def render(self, screen):
		super().render(screen)

	def update(self):
		if self.enabled:
			if self.alive:

				
				if self.collideWithPlayer():
					self.alive = False
					music.play(music.pickUpSound)
					self.player.coins += 1

				self.rect.y += self.moveDirection
				self.move_counter += 1
				if abs(self.move_counter) > 12:
					self.moveDirection *= -1
					self.move_counter *= -1

class Particle(Entity):
	def __init__(self, x, y, lifeSpan, img = None, v = [0, -1], a = [0, .1]):
		if not img:
			img = pygame.Surface((5, 5))
			pygame.draw.rect(img, (244, 0, 0), (0, 0, img.get_width(), img.get_height()))
			self.img = img


		self.lifeTime = lifeSpan
		self.lifeSpan = lifeSpan

		self.pos = [x, y]


		super().__init__(x, y, img)
		self.v = v.copy()
		self.a = a.copy()
		

	def render(self, screen):
		
		super().render(screen)


	def update(self):
		if self.enabled:
			if self.alive:
				self.lifeTime -= 1/60
				if self.lifeTime <= 0:
					self.alive = False

				self.pos[0] += self.v[0]
				self.pos[1] += self.v[1]

				self.v[0] += self.a[0]
				self.v[1] += self.a[1]

				self.rect.x = self.pos[0]
				self.rect.y = self.pos[1]

		return self.alive

class ParticleSystem():
	def __init__(self, x, y, maxNumParticles, spawnRate, particle = None):
		self.enabled = True 
		if particle:
			self.particle = particle 
		else:
			self.particle = [1, None, [0, -1], [0, .1]]
		self.pos = [x, y]
		self.maxNumParticles = maxNumParticles
		self.particles = []
		self.spawnRate = spawnRate
		self.spawnTimer = 1
		self.spawnResetValue = 1

	def update(self):
		if self.enabled:

			self.spawnTimer -= (1 - self.spawnRate)
			if self.spawnTimer <= 0 and len(self.particles) < self.maxNumParticles:
				
				self.spawnTimer = self.spawnResetValue
				import random
				for i in range(5):
					self.particles.append(Particle(self.pos[0], self.pos[1], self.particle[0], self.particle[1], [self.particle[2][0] + 2 * random.random() - 1, self.particle[2][1] + 2 * random.random() - 1], self.particle[3])) 

			for i, particle in reversed(list(enumerate(self.particles))):
				if not particle.update():
					self.particles.pop(i)

	def render(self, screen):

		for particle in self.particles:
			particle.render(screen)



class Tile():
	
	T_BG = -1
	#Enviroment
	T_Ground = 0
	T_Wall = 1
	T_OneWay = 2
	#Hazards
	T_Spikes = 201
	T_WallSpikes = 202
	T_Lava = 203

	#Enemies
	T_Enemy_Basic = 301
	T_Enemy_Flying = 302
	T_Enemy_Turret = 303
	T_Enemy_Rocket_Turret = 304

	#Tiles that spawn an object when level starts
	T_PlayerSpawn = 1001
	T_PlayerGoal = 1002
	T_Coin = 1003
	T_Key = 1004

	
	#Colors will eventually be replaced with sprites
	C_BG = (30, 20, 20)
	C_Ground = (100, 200, 10)
	C_Wall = (100, 10, 100)
	C_Spikes = (200, 100, 100)
	C_PlayerSpawn = (100, 100, 100)
	C_PlayerGoal = (100, 255, 100)
	C_Coin = (200, 200, 0)
	C_Key = (200, 100, 0)
	C_Lava = (255, 0, 0)
	C_Enemy_Basic = (100, 100, 200)
	C_Enemy_Flying = (100, 100, 255)
	C_Enemy_Turret = (0, 0, 255)
	C_Enemy_Rocket_Turret = (0, 50, 255)


	colorDict = {
	T_BG : C_BG,
	T_Ground : C_Ground,
	T_Wall : C_Wall,
	T_Spikes : C_Spikes,
	T_PlayerSpawn : C_PlayerSpawn,
	T_PlayerGoal : C_PlayerGoal,
	T_Coin : C_Coin,
	T_Key : C_Key,
	T_Lava : C_Lava,
	T_Enemy_Basic : C_Enemy_Basic,
	T_Enemy_Flying : C_Enemy_Flying,
	T_Enemy_Turret : C_Enemy_Turret,
	T_Enemy_Rocket_Turret : C_Enemy_Rocket_Turret

	}

	imgDict = {
		T_Wall : pygame.image.load(os.path.join('Images', 'Wall.png')),
		T_Ground : pygame.image.load(os.path.join('Images', 'Ground.png'))
	}


	def __init__(self, x, y, tileType):
		self.tileType = tileType
		self.rect = pygame.Rect((x, y), tileSize)
		if tileType in self.imgDict.keys():
			self.img = self.imgDict[tileType].convert()
		else:
			self.img = pygame.Surface(tileSize)
			pygame.draw.rect(self.img, self.colorDict[tileType], pygame.Rect((0, 0), tileSize))

	def render(self, screen):
		screen.blit(self.img, (self.rect.x, self.rect.y))