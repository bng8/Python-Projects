import pygame
import time
import sys
from menu import Menu
from instructions import Instructions
from credits import Credits

class MenuHandler:

	def __init__(self):
		self.PLAY_STATE = 3
		self.INSTRUCTIONS_STATE = 2
		self.CREDITS_STATE = 1
		self.MENU_STATE = 0

		self.menus = [Menu(self), Credits(self), Instructions(self)]
		self.curState = self.MENU_STATE

	def draw(self, screen):
		self.menus[self.curState].draw(screen)

	def update(self):
		if self.curState == self.PLAY_STATE:
			import Main
			sys.exit()
		self.menus[self.curState].update()

pygame.init()
size = (1024,768)
pygame.display.set_caption("Body Game")
screen = pygame.display.set_mode(size)


FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30
time_start = 0
timeS = time.time()
playing = True
handler = MenuHandler()

while playing:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False

	handler.update()
	handler.draw(screen)

	pygame.display.flip()


	if TIME_PER_FRAME - (time.time() - time_start) > .0005:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))
		timeSlept += TIME_PER_FRAME - (time.time() - time_start)