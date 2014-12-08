import pygame

class Credits:
	def __init__(self, handler):
		self.handler = handler
		self.title = pygame.transform.scale2x(pygame.image.load("res/211title.png")).convert_alpha()
		self.bgImg = pygame.image.load("res/menubg.png").convert_alpha()
		self.back = pygame.image.load("res/backicon.png")


		alpha = 30
		self.title.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

		title_font = pygame.font.SysFont("rockwell", 48, True, True)
		position_font = pygame.font.SysFont("timesnewroman", 24)
		font = pygame.font.SysFont("timesnewroman", 18)

		self.credits = title_font.render("Credits", 1, (100,0,0))
		self.strings = []
		self.strings.append(position_font.render("Lead Programmer", 1, (0, 0, 0)))
		self.strings.append(font.render("John Delaney", 1, (0, 0, 0)))
		self.strings.append(position_font.render("Assistant Lead Programmer", 1, (0, 0, 0)))
		self.strings.append(font.render("Chirayu Poudel", 1, (0, 0, 0)))
		self.strings.append(position_font.render("Graphic Designer", 1, (0, 0, 0)))
		self.strings.append(font.render("Brandon Ng", 1, (0, 0, 0)))
		self.strings.append(position_font.render("Programming", 1, (0, 0, 0)))
		self.strings.append(font.render("Tristan Hartwell", 1, (0, 0, 0)))
		self.strings.append(font.render("Max Hasenauer", 1, (0, 0, 0)))
		self.strings.append(font.render("Brandon Ng", 1, (0, 0, 0)))

	def draw(self, screen):
		screen.blit(self.bgImg, (0, 0))
		screen.blit(self.title, (180, 180))
		screen.blit(self.credits, (420,50))
		screen.blit(self.back, (400, 600))
		
		y = 175
		for ele in self.strings:
			screen.blit(ele, (100, y))
			y += 30



	def update(self):
		
		rect = self.back.get_rect().move(400,600)
		if rect.collidepoint(pygame.mouse.get_pos()):
			if pygame.mouse.get_pressed()[0]:
				self.handler.curState = 0
		
