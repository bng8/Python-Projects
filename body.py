import pygame

class Body:
	def __init__(self, pos, theta):
		self.pos = pos
		self.theta = -theta - 90
		self.img = pygame.image.load("res/guard-dead.png").convert_alpha()
		self.img = pygame.transform.flip(self.img, True, False)
		self.rect = self.img.get_rect()
		self.rect.center = (pos[0], pos[1])

	def draw(self, screen):
		rot_img = pygame.transform.rotate(self.img, self.theta)
		rot_rect = rot_img.get_rect()
		rot_rect.center = self.rect.center
		screen.blit(rot_img, rot_rect)

