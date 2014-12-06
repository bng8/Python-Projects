import pygame
import math
import astar
import pygame.gfxdraw

def rot_center(image, rect, angle):
	"""rotate an image while keeping its center"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image,rot_rect

def roundNum(num):
	if num % 1 > .5:
		return int(num)
	else:
		return math.ceil(num)

class Triangle:
	def __init__(self, pos1, pos2, pos3):
		self.pos1 = pos1
		self.pos2 = pos2
		self.pos3 = pos3

	def draw(self, screen):
		#draw triangle
		pygame.gfxdraw.filled_trigon(screen, round(self.pos1[0]), round(self.pos1[1]), round(self.pos2[0]), round(self.pos2[1]), round(self.pos3[0]), round(self.pos3[1]), (255, 255, 0,  180))


class Line:
	def __init__(self, posS,posE):
		self.startPos = posS
		self.endPos = posE
		self.distX = posE[0] - posS[0]
		self.distY = posE[1] - posS[1]
		self.mag = (self.distX ** 2 + self.distY ** 2) ** ( 1/ 2)

	def draw(self, screen, color):
		#draw line
		pygame.draw.line(screen, color, self.startPos, self.endPos)

	def __eq__(self, other):
		if self.startPos[0] == other.startPos[0] and self.startPos[1] == other.startPos[1] and self.endPos[0] == other.endPos[0] and self.endPos[1] == other.endPos[1]:
			return True
		else:
			return False

	def nearestIntersection(self, level):
		t1, t2 = 100, 100
		#search for intersection of line and any wall
		for wall in level.walls:
			
			wallX = wall.x
			wallY = wall.y
			wallDX = wall.width
			wallDY = 0
			tmp = 0
			tmp2 = 0
			
			#top line segment of wall
			#solve two equations for two unkowns of the the two vectors(ray and wall segment)
			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				if self.distY != 0:
					tmp2 = (wallY - self.startPos[1]) / self.distY
			#find minimum step to find a wall(assuming it is on line segment[tmp being step of segment], and it is forwards)
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2

			#left wall segment
			wallX = wall.x
			wallY = wall.y
			wallDX = 0
			wallDY = wall.height

			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				tmp = -1
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2

			#right wall segment
			wallX = wall.x + wall.width
			wallY = wall.y + wall.height
			wallDX = 0
			wallDY = -wall.height
			
			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				tmp = -1
			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2
			
			#bottom wall segment
			wallX = wall.x + wall.width
			wallY = wall.y + wall.height
			wallDX = -wall.width
			wallDY = 0

			try:
				tmp = (self.distY * (-wallX + self.startPos[0]) + self.distX * (-self.startPos[1] + wallY)) / ((self.distY * wallDX) - (self.distX * wallDY))
				tmp2 = (wallX + wallDX * tmp - self.startPos[0]) / self.distX
			except:
				if self.distY != 0:
					tmp2 = (wallY - self.startPos[1]) / self.distY

			if tmp2 < t1 and tmp > 0 and tmp < 1 and tmp2 > 0:
				t1 = tmp2
		#get new line that ends at closest intersection point and return it
		line = Line(self.startPos, (self.startPos[0] + self.distX * t1, self.startPos[1] + self.distY * t1))
		return line

	def changeMag(self, mag):
		#change the length of a line while preserving direction
		unit = (self.distX / self.mag, self.distY / self.mag)
		self.endPos = (self.startPos[0] + unit[0] * mag, self.startPos[1] + unit[1] * mag)

	def getAngle(self, theta):
		#vector opposite of where we are facing
		#flip sin and cos because we take 0 degrees at top of circle
		vec = [-math.sin(math.radians(theta)), -math.cos(math.radians(theta))]
		
		#get magnitude of vector where we are facing(always one[sin^2 + cos^2 = 1])
		magVec = 1
		
		#cross product of vector for each ray and vector we are facing
		val = vec[0] * self.distY - vec[1] * self.distX

		#try except is for rounding errors(precautionary)
		try:
			#cross product rule
			ang = math.asin(val / (magVec * self.mag))
		except:
			ang = math.asin(round(val / (magVec * self.mag)))

		#return angle with respect to vector opposite of direction of motion
		return ang * 180 / math.pi


	def __repr__(self):
		return "endPos: " + str(self.distX) + ", " + str(self.distY) + "  angle" + str(self.getAngle(math.pi))




class Guard:
	def __init__(self, pos_, path_, map_, speed, rang, fov):
		#same thing as player; these two are used to make it look like they're walking
		self.x=0

		#initialize vars
		self.path = path_
		self.level = map_
		self.speed = speed
		self.range = rang
		self.fov = fov
		self.triangles = []
		self.pos = [pos_[0], pos_[1]]
		self.img = [pygame.image.load("res/guard-left.png").convert_alpha(), pygame.image.load("res/guard-right.png").convert_alpha()]
		self.imgStanding = pygame.image.load("res/guard-standing.png").convert_alpha()
		self.guardRect = self.img[0].get_rect()
		self.guardRect.center = self.pos
		self.startPoint = self.guardRect.center[0], self.guardRect.center[1]
		self.searching = False
		self.pathFound = False
		self.standing = False
		self.mandate = False


	def initAStar(self):
		self.star = astar.AStar(self.level.getRectGrid(), None, None)

	def draw(self, screen):
		#rotate the image of the guard
		if not self.standing:
			rot_img, self.guardRect = rot_center(self.img[0], self.guardRect, self.theta)
		else:
			rot_img, self.guardRect = rot_center(self.imgStanding, self.guardRect, self.theta)

		#draw guard on screen
		screen.blit(rot_img, self.guardRect)

		pygame.draw.rect(screen, (255, 0, 0), self.collisionRect,1)

		points = [self.guardRect.center]
		for tri in self.triangles:
			points.append(tri.pos3)
			points.append(tri.pos1)
		pygame.gfxdraw.filled_polygon(screen, points, (255,255, 0, 128))


	def generateRays(self):
			#get the direction of movement
			dirVec = (-math.sin(math.radians(self.theta)), -math.cos(math.radians(self.theta)))
			magVec = (dirVec[0] ** 2 + dirVec[1] ** 2) ** (1 / 2)

			#trace a ray to each of the four corners of the walls
			#check to make sure that region is in your field of view
			#dot product rule to get the angle between movement and angle to corner
			#add ones that are in the field of view
			#cut off the rays at any intersection 
			for wall in self.level.walls:
				#create a line from the guard to a wall corner
				#top left corner
				line = Line(self.guardRect.center, (wall.x, wall.y))
				#get angle between that line and the line of movement(dot product rule)
				if -1 <= ((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec))) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))

				#top right corner
				line = Line(self.guardRect.center, (wall.x + wall.width, wall.y))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))

				#bottom left
				line = Line(self.guardRect.center, (wall.x, wall.y + wall.height))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))
				
				#bottom right
				line = Line(self.guardRect.center, (wall.x + wall.width, wall.y + wall.height))
				if -1 <= (dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)) <= 1:
					ang = math.acos((dirVec[0] * line.distX + (dirVec[1] * line.distY)) / (math.fabs(line.mag) * math.fabs(magVec)))
					ang = ang * 180 / math.pi
					ang = math.fabs(ang)
					if ang < self.fov:
						self.rays.append(line.nearestIntersection(self.level))
		
			#add rays at edge of field of view, and one in the center(case in which no walls are in view)
			self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta + self.fov)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta + self.fov)) * self.range)).nearestIntersection(self.level))
			self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta - self.fov)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta - self.fov)) * self.range)).nearestIntersection(self.level))
			#self.rays.append(Line(self.guardRect.center, (self.guardRect.center[0] - math.sin(math.radians(self.theta)) * self.range, self.guardRect.center[1] - math.cos(math.radians(self.theta)) * self.range)).nearestIntersection(self.level))

			#normalize all rays to a maximum length based on view range
			for ray in self.rays:
				if ray.mag > self.range:
					ray.changeMag(self.range)

			#sort rays based on their angle with respect to direction of motion
			self.rays = sorted(self.rays, key = lambda x: x.getAngle(self.theta))
		
			#create triangles formed by adjecent rays in the list
			for i in range(1, len(self.rays)):
				self.triangles.append(Triangle(self.rays[i].endPos, self.rays[i].startPos, self.rays[i - 1].endPos))

	def dot(self, v0, v1):
		return v0[0] * v1[0] + v0[1] * v1[1]

	def vecSub(self, p1, p2):
		return (p1[0] - p2[0], p1[1] - p2[1])


	def checkCollision(self, playerRect):
		point = playerRect.center
		for tri in self.triangles:
			v0 = self.vecSub(tri.pos2, tri.pos1)
			v1 = self.vecSub(tri.pos3, tri.pos1)
			v2 = self.vecSub(point, tri.pos1)

			dot00 = self.dot(v0, v0)
			dot01 = self.dot(v0, v1)
			dot02 = self.dot(v0, v2)
			dot11 = self.dot(v1, v1)
			dot12 = self.dot(v1, v2)

			if dot00 * dot11 - dot01 * dot01 != 0:
				invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
				u = (dot11 * dot02 - dot01 * dot12) * invDenom
				v = (dot00 * dot12 - dot01 * dot02) * invDenom

				if u >= 0 and v >= 0 and u + v < 1:
					return True
		return False

	def canWalkStraight(self, tarRect):
		line = Line(self.guardRect.center, tarRect.center)
		line2 = line.nearestIntersection(self.level)

		if line2 == line or line2.mag > line.mag:
			return True
		else:
			return False


	def update(self, playerRect, bodies):
		self.magMove = [0, 0]
		thet = 0
		self.rays = []
		self.triangles = []

		if len(self.path) > 0:
		#get direction of movement based on path
			self.standing = False
			dirMove = (self.startPoint[0] - self.path[0][0], self.startPoint[1] - self.path[0][1])
			dirMove2 = (self.pos[0] - self.path[0][0], self.pos[1] - self.path[0][1])
			
			#get unit vector for movement
			mag = ((dirMove[0] ** 2) + (dirMove[1] ** 2)) ** (1/2)

			#set the class var to the movement determine angle
			if mag != 0: 
				self.magMove[0], self.magMove[1] = dirMove[0] / mag, dirMove[1] / mag
				thet = math.asin(dirMove[0]/ mag)
			#adjust angle based of the direction of movement
			if dirMove[1] > 0 and dirMove[0] < 0:
				thet = math.pi - thet
			if dirMove[1] > 0 and dirMove[0] >= 0:
				thet = math.pi - thet

			#convert to degrees and assign to class var
			self.theta = (-thet * 180 / math.pi) + 180

			#if guard reaches their desired path, cycle the path points
			if math.fabs(self.path[0][0] - self.guardRect.center[0]) <= 6 and math.fabs(self.path[0][1] - self.guardRect.center[1]) <= 6:
				self.startPoint = [self.path[0][0], self.path[0][1]]
				self.pos = [self.path[0][0], self.path[0][1]]
				self.guardRect.center = (self.path[0][0], self.path[0][1])
				tmp = self.path.pop(0)
				if not self.pathFound:
					self.path.append(tmp)
		#	elif dirMove2[0] != 0 and dirMove2[1] != 0 and (dirMove[0] / dirMove2[0] < 0 or dirMove[1] / dirMove2[1] < 0):
		#		self.pos = [self.path[0][0], self.path[0][1]]

			self.x+=1
			if self.x == 10:
				self.img.append(self.img.pop(0))
				self.x = 0

			#move the guard based on position
			#move pos based on speed
			self.pos[0], self.pos[1] = self.pos[0] - (self.magMove[0] * self.speed), self.pos[1] - (self.magMove[1] * self.speed)
			self.guardRect.center = self.pos[0], self.pos[1]
			self.collisionRect = pygame.Rect(self.pos[0], self.pos[1], 1, 1)

		else:
			self.theta += 2
			if not self.standing:
				self.searching = False
				self.pathFound = False
				self.standing = True
				self.initAStar()

		#start ray-tracing vision
		self.generateRays()

		if self.searching and self.star.notFound:
				self.pathTmp = self.star.pathFind(.1)
				if not self.star.notFound:
					self.path = self.pathTmp
					self.startPoint = self.guardRect.center
					self.pathFound = True
					grd = self.level.getRectGrid()

					#for ele in self.path:
					#	grd[ele[0]][ele[1]] = 5

					for i in range(len(self.path)):
						self.path[i] = self.path[i][1], self.path[i][0]

					#for ele in grd:
					#	print(ele)

					for i in range(len(self.path)):
						self.path[i] = self.path[i][0] * 32, self.path[i][1] * 32

		playerSeen = self.checkCollision(playerRect)
		if playerSeen and self.canWalkStraight(playerRect):
			self.path = [playerRect.center]
			pathFound = True
		elif (playerSeen and not self.searching and not self.pathFound) or self.mandate:
			self.searching = True
			self.star.startPath((roundNum(self.guardRect.center[1] / 32), roundNum(self.guardRect.center[0] / 32)), (roundNum(playerRect.center[1] / 32), roundNum(playerRect.center[0] / 32)))

		if not playerSeen:
			for body in bodies:
				if self.checkCollision(body.rect):
					self.searching = True
					self.star.startPath((roundNum(self.guardRect.center[1] / 32), roundNum(self.guardRect.center[0] / 32)), (roundNum(body.rect.center[1] / 32), roundNum(body.rect.center[0] / 32)))
					#self.star.startPath((roundNum(self.guardRect.center[1] / 16), roundNum(self.guardRect.center[0] / 16)), (roundNum(body.rect.center[1] / 16), roundNum(body.rect.center[0] / 16)))

		
		for wall in self.level.walls:
			if self.collisionRect.colliderect(wall):
				self.pos[0], self.pos[1] = self.pos[0] + 2 * (self.magMove[0] * self.speed), self.pos[1] + 2 * (self.magMove[1] * self.speed)
				self.mandate = True
				self.initAStar()
				break
		

		
