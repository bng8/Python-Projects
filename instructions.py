import pygame

class Instructions:
	def __init__(self, handler):
		self.handler = handler
		self.title = pygame.transform.scale2x(pygame.image.load("res/211title.png")).convert_alpha()
		self.bgImg = pygame.image.load("res/menubg.png").convert_alpha()

		alpha = 30
		self.title.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

		title_font = pygame.font.SysFont("rockwell", 48, True, True)
		font = pygame.font.SysFont("timesnewroman", 18)

		self.instructions = title_font.render("Instructions", 1, (100,0,0))
		self.strings = []
		self.strings.append(font.render("( W ) Move in the direction of the Cursor", 1, (0, 0, 0)))
		self.strings.append(font.render("( D ) Move in the direction opposite to the Cursor", 1, (0, 0, 0)))
		self.strings.append(font.render("( A ) Move in the direction perpendicular to the left of the Cursor", 1, (0, 0, 0)))
		self.strings.append(font.render("( S ) Move in the direction perpendicular to the right of the Cursor", 1, (0, 0, 0)))
		self.strings.append(font.render("( P ) Pause", 1, (0, 0, 0)))
		self.strings.append(font.render("( Left Click ) Stab", 1, (0, 0, 0)))
		self.strings.append(font.render("( Action Bar ) Pick up a dead body OR hold to unlock a safe", 1, (0, 0, 0)))
		self.strings.append(font.render("Objective: Get to the safe(s) and obtain the gold bar inside. Then return to the door with the keys to move on to the", 1, (0, 0, 0)))
		self.strings.append(font.render("next level. Make sure to avoid being caught by the Guards, by avoiding their flashlights and/or taking them out. HINT: You", 1, (0, 0, 0)))
		self.strings.append(font.render("can use dead bodies to get the attention of the guards!", 1, (0, 0, 0)))

	def draw(self, screen):
		screen.blit(self.bgImg, (0, 0))
		screen.blit(self.title, (180, 180))
		screen.blit(self.instructions, (380,50))

		y = 175
		for ele in self.strings:
			screen.blit(ele, (100, y))
			y += 30



	def update(self):
		
		#pseudo code
		'''
		rect = self.backButton.get_rect().move(self.poisitionOfButton)
		if rect.collidepoint(pygame.mouse.get_pos()):
			if pygame.getMousePressed()[0]:
				self.handler.curState = self.handler.menuState
		'''
