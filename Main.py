import pygame
import sys
import time
import urllib
import os
import urllib.request
import io
from safe import Safe
from player import Player
from guard import Guard
from level_builder import LevelBuilder

size = (1024, 768)
xCenter, yCenter= size[0] / 2, size[1] / 2

#initialize window
screen = pygame.display.set_mode(size,pygame.SRCALPHA)

FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30
time_start = 0
timeS = time.time()
playing = True
#bools for keys
keys = {"W": False, "S" : False, "D" : False, "A" : False, "P" : False, "SPACE" : False}

def outlinedText(text, font, colorIn, colorOut, width, alpha = 255, back = None, pos = (0, 0)):

	textI = font.render(text, 1, colorIn)
	textO = font.render(text, 1, colorOut)

	newSurf = pygame.Surface((textI.get_size()[0] + width * 2, textI.get_size()[1] + width * 2))

	if back:
		newSurf.blit(back, pos)

	newSurf.blit(textO, (0, 0))
	newSurf.blit(textO, (width * 2, 0))
	newSurf.blit(textO, (0, width * 2))
	newSurf.blit(textO, (width * 2, width * 2))
	newSurf.blit(textO, (width, 0))
	newSurf.blit(textO, (width * 2, 2))
	newSurf.blit(textO, (0, width))
	newSurf.blit(textO, (width * 2, width))
		
	newSurf.blit(textI, (width, width))

	newSurf.set_alpha(int(alpha))

	return newSurf

def levelFileReader(filename):
	#variables
	levelRects=[]      #array to hold the rectangle object
	Speed=0
	Range=0
	fov=0
	paths=[]           #array to hold the paths of number of guards for the level
	guards = []
	safes = []

	#open file
	level_file = open(filename + '.txt')
	#read file
	level_str = level_file.read()
	level_str = level_str.strip()
	#close file
	level_file.close()
	
	player = Player((612, 348), 5, None)

	#taking the string and breaking it up at the guard into the rect info and the guard info
	level_list = level_str.split('Guard:')
	rect_list = level_list[0].split('\n')[:-1]
	#breaking up the info for the separate rect if then appending new rects for each line
	for elm in rect_list:
		points = elm.split(',')
		for i in range(len(points)):
			points[i] = int(points[i])
		levelRects.append(pygame.Rect((points[0], points[1], points[2], points[3])))

	#prepping the guard info
	guard_lines = level_list[1].split('\n')[1:]
	speed = guard_lines[0] #first line
	rang = guard_lines[1] #second line
	fov = guard_lines[2] #third line
	#putting the paths into an array
	paths = guard_lines[3:]
	for ele in paths:
		path = ele.split(",")
		for i in range(len(path)):
			tmp = path[i].strip().split(" ")
			path[i] = int(tmp[0]), int(tmp[1])
		guards.append(Guard(path[0], path, None, int(speed), int(rang), int(fov)))

	#add borders around screen(in every level)
	levelRects.append(pygame.Rect(0,0,size[0], 32))
	levelRects.append(pygame.Rect(0,size[1] - 32,size[0], 32))
	levelRects.append(pygame.Rect(0, 32, 32, size[1] - 32))
	levelRects.append(pygame.Rect(size[0] - 32, 32, 32, size[1] - 32))

	##hard coded, safes will be in txt file
	safes.append(Safe((50, 50)))
	safes.append(Safe((750, 200)))
	safes.append(Safe((700, 650)))

	return LevelBuilder(pygame.image.load("res/background-img.jpg").convert_alpha(), levelRects, guards, player, safes)


pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

level= levelFileReader("Levels/level1")

pygame.font.init()
font = pygame.font.SysFont('timesnewroman', 100)
pausedText = font.render("PAUSED", 1, (255,255,255))
font2 = pygame.font.SysFont("timesnewroman", 36)
continueText = font2.render("Press spacebar to continue", 1, (255,255,255))
font3 = pygame.font.SysFont('timesnewroman', 175)

pygame.mixer.init()
snd1 = pygame.mixer.Sound('tone2.wav')
#snd2 = pygame.mixer.Sound('tone1.wav')

timeSlept = 0
timePStart = time.time()
textInc = 0
back = None
#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()
	#check for key and mouse event
	#Polling input
	if level.gameOver == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					playing = False
				if event.key == pygame.K_w:
					keys['W'] = True
				if event.key == pygame.K_s:
					keys['S'] = True
				if event.key == pygame.K_a:
					keys['A'] = True
				if event.key == pygame.K_d:
					keys['D'] = True
				if event.key == pygame.K_p:
					keys['P'] = not keys['P']
				if event.key == pygame.K_SPACE:
					keys['SPACE'] = True
				if event.key == pygame.K_k:
					snd2.play()
				if event.key == pygame.K_l:
					snd1.play()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					keys['W'] = False
				if event.key == pygame.K_s:
					keys['S'] = False
				if event.key == pygame.K_a:
					keys['A'] = False
				if event.key == pygame.K_d:
					keys['D'] = False
				if event.key == pygame.K_SPACE:
					keys['SPACE'] = False

		#update everything if not paused
		if not keys['P']:
			level.update(keys)
				
		#make screen black(erase screen)
		screen.fill((0,0,0))

		level.draw(screen)

		if keys['P']:
			screen.blit(outlinedText("PAUSED", font, (255 , 255, 255), (0,0,0), 2, 255, screen, (-320, -300)), (320,300))
			screen.blit(outlinedText("Press spacebar to continue...", font2, (255 , 255, 255), (0,0,0), 2, 255, screen, (-320, -400)), (320 ,400))

	elif level.gameOver == 1:

		if textInc == 0:
			back = screen

		textInc += .2
		
		if textInc > 24:
			textInc = 0
			level = levelFileReader("Levels/level1")

		screen.blit(outlinedText("Game Over", font3, (255 , 0, 0), (0,0,0), 3, textInc, back, (-100, -100)), (100, 100))

	elif level.gameOver == 2:

		if textInc == 0:
			back = screen

		textInc += .2

		if textInc > 24:
			textInc = 0
			level = levelFileReader("Levels/level1")

		screen.blit(outlinedText("Level", font3, (255 , 0, 0), (0,0,0), 3, textInc, back, (-350, -100)), (350, 100))
		screen.blit(outlinedText("Complete", font3, (255 , 0, 0), (0,0,0), 3, textInc, back, (-200, -300)), (200, 300))

	pygame.display.flip()
	'''
	#print out time remaning/sec
	if time.time() - timePStart > 1:
		timePStart = time.time()
		print(timeSlept)
		timeSlept = 0
	'''
	#print(TIME_PER_FRAME - (time.timwe() - time_start))
	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > .0005:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))
		timeSlept += TIME_PER_FRAME - (time.time() - time_start)