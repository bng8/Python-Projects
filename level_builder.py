import pygame
import random
import time
import astar
from safe import Safe
from body import Body

class LevelBuilder():
	

	def __init__(self, floor_img, walls, guards, player, safes, door_coordinates, door_rotation):
		self.walls = walls
		self.floorList = [pygame.image.load("res/background-img.jpg").convert_alpha(), pygame.image.load("res/background-img2.jpg").convert_alpha(),
		pygame.image.load("res/background-img3.jpg").convert_alpha(),pygame.image.load("res/background-img4.jpg").convert_alpha(),
		pygame.image.load("res/background-img5.jpg").convert_alpha()]
		self.floor_img = random.choice(self.floorList)
		self.guards = guards
		for i in range(len(self.guards)):
			self.guards[i].level = self
			self.guards[i].initAStar()
		self.player = player	
		self.door_img = pygame.image.load("res/door.png").convert_alpha()
		self.door_rotation = door_rotation
		if self.door_rotation == 1:
			self.door_img = pygame.transform.rotate(self.door_img, 90)
		self.door_coordinates = door_coordinates
		self.doorRect = self.door_img.get_rect()
		self.doorRect = self.doorRect.move(self.door_coordinates[0], self.door_coordinates[1])
		print(self.doorRect.center)
		self.player.level = self
		self.wallImgList = [pygame.image.load("res/wall_horizontal.jpg").convert_alpha(), pygame.image.load("res/wall_horizontal2.jpg").convert_alpha()]
		self.wallImgHor= random.choice(self.wallImgList)
		self.wallImgVert = pygame.transform.rotate(self.wallImgHor, 90)
		self.bodies = []
		self.cooldown = 0
		self.safes = safes
		self.keys = 0
		self.keyImg = pygame.image.load("res/goldbar.png").convert_alpha()
		grd = self.getRectGrid()
		self.gameOver = 0


	def update(self, keys):
		self.player.update(keys)
		for guard in self.guards:
			guard.update(self.player.playerRect, self.bodies)

		#check for if the player kills a guard
		for i in range(len(self.guards)):
			#if rects collide(will change when we have attack animation)
			if self.player.collisionRect.colliderect(self.guards[i].guardRect):
				if self.guards[i].playerSeen:
					self.gameOver = 1
					
					
				if self.player.attacking and not self.guards[i].playerSeen:
					#get the guard/remove it
					tmp = self.guards.pop(i)
					#add body in guards position
					self.bodies.append(Body(tmp.pos, tmp.theta))
					break

		if self.cooldown > 0:
			self.cooldown -= 1

		for safe in self.safes:
			if self.player.collisionRect.colliderect(safe.rect) and not safe.objectRetrieved and keys["SPACE"]:
				safe.update()
				if safe.objectRetrieved:
					self.keys += 1
				return
			else:
				safe.progress = 0
				safe.bar = None

		if keys["SPACE"]:
			if self.player.carrying and self.cooldown == 0:
				self.bodies.append(Body(self.player.playerRect.center, self.player.theta))
				self.player.carrying = False
				self.cooldown = 10
			else:
				for i, body in enumerate(self.bodies):
					if not self.player.carrying and self.player.playerRect.colliderect(body.rect) and self.cooldown == 0:
						self.player.attacking = False
						self.player.carrying = True
						self.bodies.pop(i)
						self.cooldown = 10

		print(self.keys, " - ", len(self.safes))
		if self.keys == len(self.safes) and self.player.playerRect.colliderect(self.doorRect):
			print("hello")
			self.gameOver = 2

	def draw(self, screen):
		screen.blit(self.floor_img, (0,0))

		for body in self.bodies:
			body.draw(screen)

		self.player.draw(screen)
		for guard in self.guards:
			guard.draw(screen)

		for safe in self.safes:
			safe.draw(screen)

		x=0
		
		for wall in self.walls:
			#when the wall is wider than it is long, so that the brick pattern still works
			if(wall.right-wall.left>32):
				for i in range(wall.left-32, wall.right-32, 32):
					screen.blit(self.wallImgHor, (wall.left+x, wall.top))
					x+=32
					
			#when the wall is longer than it is wide
			if(wall.bottom-wall.top > 32):
				for i in range(wall.top-32, wall.bottom-32, 32):
					screen.blit(self.wallImgVert, (wall.left, wall.top+x))
					x+=32
			x=0
			pygame.draw.rect(screen, (0, 0, 0), wall, 3)

		
		#Drawing keys after safes are emptied
		keyImg = self.keyImg
		x = 0

		for i in range(self.keys):
			screen.blit(keyImg,(775+(60 * i), 0))


		for safe in self.safes:
			if not safe.objectRetrieved and self.player.collisionRect.colliderect(safe.rect):
				safe.drawBar(screen)

		screen.blit(self.door_img, self.door_coordinates)

	def getRectGrid(self):
		"""Returns a 64x48 matrix of 0s and 1s, where 1s denote the presence of a wall"""
		
		GridList = [[0 for x in range(32)] for y in range(24)]
		for wall in self.walls:
			left_coordinate, right_coordinate = int(wall.left/32), int(wall.right/32)
			top_coordinate, bottom_coordinate = int(wall.top/32), int(wall.bottom/32)
			
			for i in range(left_coordinate, right_coordinate):
				for j in range(-1, (bottom_coordinate-top_coordinate)+1):
					if top_coordinate + j>= 0 and top_coordinate+j<=23:
						GridList[top_coordinate + j][i] = 1
			
			for i in range(top_coordinate, bottom_coordinate):
				for j in range(-1, (right_coordinate-left_coordinate)+1):
					if left_coordinate+j >= 0 and left_coordinate+j<=31:
						GridList[i][left_coordinate+j] = 1

			if bottom_coordinate - top_coordinate > right_coordinate - left_coordinate:
				if 0 < (bottom_coordinate) < 24 and 0 < right_coordinate - 1 < 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1
				if 0 < (bottom_coordinate) < 24 and 0 < right_coordinate + 1 < 31:
					GridList[bottom_coordinate][left_coordinate + 1] = 1

				if 0 < (top_coordinate) < 24 and 0 < right_coordinate - 1 < 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1
				if 0 < (top_coordinate) < 24 and 0 < right_coordinate + 1 < 31:
					GridList[top_coordinate][left_coordinate + 1] = 1
			
			else:
				if 0 < (bottom_coordinate - 2) < 24 and 0 < left_coordinate - 1< 31:
					GridList[bottom_coordinate - 2][left_coordinate - 1] = 1
				if 0 < (bottom_coordinate) < 24 and 0 < left_coordinate  - 1< 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1

				if 0 < (bottom_coordinate - 2) < 24 and 0 < right_coordinate < 31:
					GridList[bottom_coordinate - 2][right_coordinate] = 1
				if 0 < (bottom_coordinate) < 24 and 0 < right_coordinate  < 31:
					GridList[bottom_coordinate][right_coordinate] = 1
		
		'''
		GridList = [[0 for x in range(64)] for y in range(48)]
		for wall in self.walls:
			left_coordinate, right_coordinate = int(wall.left/16), int(wall.right/16)
			top_coordinate, bottom_coordinate = int(wall.top/16), int(wall.bottom/16)
			
			for i in range(left_coordinate, right_coordinate):
				for j in range(-2, (bottom_coordinate-top_coordinate)+2):
					if top_coordinate + j>= 0 and top_coordinate+j<=47:
						GridList[top_coordinate + j][i] = 1
			
			for i in range(top_coordinate, bottom_coordinate):
				for j in range(-2, (right_coordinate-left_coordinate)+2):
					if left_coordinate+j >= 0 and left_coordinate+j<=63:
						GridList[i][left_coordinate+j] = 1

			if bottom_coordinate - top_coordinate > right_coordinate - left_coordinate:
				if 0 < (bottom_coordinate) < 48 and 0 < right_coordinate - 1 < 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1
				if 0 < (bottom_coordinate) < 48 and 0 < right_coordinate + 1 < 31:
					GridList[bottom_coordinate][left_coordinate + 1] = 1

				if 0 < (top_coordinate) < 48 and 0 < right_coordinate - 1 < 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1
				if 0 < (top_coordinate) < 48 and 0 < right_coordinate + 1 < 31:
					GridList[top_coordinate][left_coordinate + 1] = 1
			
			else:
				if 0 < (bottom_coordinate - 2) < 48 and 0 < left_coordinate - 1< 31:
					GridList[bottom_coordinate - 2][left_coordinate - 1] = 1
				if 0 < (bottom_coordinate) < 24 and 0 < left_coordinate  - 1< 31:
					GridList[bottom_coordinate][left_coordinate - 1] = 1

				if 0 < (bottom_coordinate - 2) < 24 and 0 < right_coordinate < 31:
					GridList[bottom_coordinate - 2][right_coordinate] = 1
				if 0 < (bottom_coordinate) < 24 and 0 < right_coordinate  < 31:
					GridList[bottom_coordinate][right_coordinate] = 1
		'''
			
		return GridList

#path finding test(IGNORE)
'''
size = (1024, 768)
rectForWalls = []
guards = []
rectForWalls = [pygame.Rect((0,352,368,32)), pygame.Rect((352,0,32,224)),
                        pygame.Rect((528,0,32,448)), pygame.Rect((702,432,336,32))]

rectForWalls.append(pygame.Rect(0,0,size[0], 32))
rectForWalls.append(pygame.Rect(0,size[1] - 32,size[0], 32))
rectForWalls.append(pygame.Rect(0, 32, 32, size[1] - 32))
rectForWalls.append(pygame.Rect(size[0] - 32, 32, 32, size[1] - 32))

level_one = LevelBuilder(rectForWalls, guards)
grd = level_one.getRectGrid()
star = astar.AStar(grd.copy(), (4,4), (40,4))
start = (4,4)

star.startPath(start, (20,4))

timeStart = time.time()
for i in range(25):
	if not star.notFound:
		break
	path = star.pathFind(.01)


print(path)
print(time.time() - timeStart)

for ele in path:
	grd[ele[0]][ele[1]] = 5

for ele in grd:
	print(ele)
'''
