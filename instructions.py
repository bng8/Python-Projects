import pygame

class Instructions:
	def __init__(self, handler):
		self.handler = handler
		self.title = pygame.transform.scale2x(pygame.image.load("res/211title.png")).convert_alpha()
		self.bgImg = pygame.image.load("res/menubg.png").convert_alpha()

		alpha = 30
		self.title.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

	def draw(self, screen):
		screen.blit(self.bgImg, (0, 0))
		screen.blit(self.title, (180, 180))


	def update(self):
		pass