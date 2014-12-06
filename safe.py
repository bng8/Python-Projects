
import pygame

class Safe():
	def __init__(self, pos):
		self.img = pygame.image.load("res/safe.png").convert_alpha()
		self.pos = pos
		self.objectRetrieved = False
		self.rect = self.img.get_rect()
		self.rect.center = (pos[0], pos[1])


	def draw(self, screen):
		if self.objectRetrieved:
			self.img = pygame.image.load("res/safe_retrieved.png").convert_alpha()
		screen.blit(self.img, self.pos)


	def retrieveKey(self, screen):
		progressArea = pygame.Surface((64,20))
		screen.blit(progressArea, (self.pos[0],self.pos[1]-25))

		progress = 0
		while progress<1:
			pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.pos[0],(self.pos[1]-25), 64*progress,20))
			progressArea.fill((0,0,0))
			progress+=0.00005
			pygame.display.update(pygame.Rect(self.pos[0],(self.pos[1]-25), 64*progress,20))
		if progress >= 1:
			self.objectRetrieved = True