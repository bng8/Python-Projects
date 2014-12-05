import pygame
import sys
import time
import urllib
import os
import urllib.request
import io
from player import Player
from guard import Guard
from level_builder import LevelBuilder

size = (1024, 768)
xCenter, yCenter= size[0] / 2, size[1] / 2

#initialize window
screen = pygame.display.set_mode(size)

FRAMES_PER_SECOND = 30
TIME_PER_FRAME = 1.0 / 30
time_start = 0
timeS = time.time()
playing = True
#bools for keys
keys = {"W": False, "S" : False, "D" : False, "A" : False, "SPACE" : False}

def levelFileReader(filename):
	#variables
	levelRects=[]      #array to hold the rectangle object
	Speed=0
	Range=0
	fov=0
	paths=[]           #array to hold the paths of number of guards for the level
	guards = []

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

	return LevelBuilder(pygame.image.load("res/background-img.jpg").convert_alpha(), levelRects, guards, player)
	

pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

level= levelFileReader("Levels/level1")

pygame.font.init()
font = pygame.font.SysFont('timesnewroman', 100)
pausedText = font.render("PAUSED", 1, (255,255,255))
font2 = pygame.font.SysFont("timesnewroman", 36)
continueText = font2.render("Press spacebar to continue", 1, (255,255,255))

timeSlept = 0
timePStart = time.time()
#Main Game Loop
while playing == True:
	#get the time at start of this specific cycle of loop
	time_start = time.time()
	#check for key and mouse event
	#Polling input
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
			if event.key == pygame.K_SPACE:
				keys['SPACE'] = not keys['SPACE']
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				keys['W'] = False
			if event.key == pygame.K_s:
				keys['S'] = False
			if event.key == pygame.K_a:
				keys['A'] = False
			if event.key == pygame.K_d:
				keys['D'] = False

	#update everything if not paused
	if not keys['SPACE']:
		level.update(keys)
			
	#make screen black(erase screen)
	screen.fill((0,0,0))

	level.draw(screen)

	if keys['SPACE']:
		screen.blit(pausedText, (320,300))
		screen.blit(continueText, (320 ,400))

	#update display
	pygame.display.flip()


	'''
	#print out time remaning/sec
	if time.time() - timePStart > 1:
		timePStart = time.time()
		print(timeSlept)
		timeSlept = 0
	'''
	#print(TIME_PER_FRAME - (time.time() - time_start))
	#sleep to maintain a constant framerate of 30 fps
	if TIME_PER_FRAME - (time.time() - time_start) > .0002:
		time.sleep(TIME_PER_FRAME - (time.time() - time_start))
		timeSlept += TIME_PER_FRAME - (time.time() - time_start)