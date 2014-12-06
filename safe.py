
import pygame

class Safe():
	def __init__(self, pos):
		self.img = pygame.image.load("res/safe.png").convert_alpha()
		self.imgR = pygame.image.load("res/safe_retrieved.png").convert_alpha()
		self.pos = pos
		self.objectRetrieved = False
		self.rect = self.img.get_rect()
		self.rect.x, self.rect.y = pos[0], pos[1]
		self.progress = 0
		self.progBack = pygame.Rect(pos[0], pos[1] - 25, 64, 20)
		self.bar = None


	def draw(self, screen):
		if self.objectRetrieved:
			self.img = self.imgR
		screen.blit(self.img, self.rect)

	def drawBar(self, screen):
		if self.bar:
			pygame.draw.rect(screen, (0, 0, 0), self.progBack)
			pygame.draw.rect(screen, (255,255,255), self.bar)

	def update(self):
		if self.progress < 1:
			self.bar = pygame.Rect(self.pos[0],(self.pos[1]-25), 64*self.progress,20)
			self.progress+= 1 / 90
		if self.progress >= 1:
			self.objectRetrieved = True
