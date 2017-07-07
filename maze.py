import pygame
import sys
import random

TOTAL = 600
WIDTH = TOTAL
HEIGHT = TOTAL
CELLSIZE = 20

ROWS = HEIGHT / CELLSIZE
COLS = WIDTH / CELLSIZE

global cellindex
global cells

cells = []

pygame.init()

DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 100
clock = pygame.time.Clock()
class Cell():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.top = True
		self.right = True
		self.bottom = True
		self.left = True
		self.visited = False

		self.t = True
		self.r = True
		self.b = True
		self.l = True

	def FindNeighbors(self):
		global cells
		global cellindex
		if self.x == 0:
			self.l = False
		if self.x == COLS - 1:
			self.r = False
		if self.y == 0:
			self.t = False
		if self.y == ROWS - 1:
			self.b = False
		potentials = []
		
		if self.l:
			left_cell = cells[(self.x-1) + self.y * COLS]
			if left_cell.visited == False:
				potentials.append(left_cell)
		if self.r:
			right_cell = cells[(self.x+1) + self.y * COLS]
			if right_cell.visited == False:
				potentials.append(right_cell)
		if self.t:
			top_cell = cells[(self.x) + (self.y - 1 ) * COLS]
			if top_cell.visited == False:
				potentials.append(top_cell)
		if self.b:
			bottom_cell = cells[(self.x) + (self.y + 1) * COLS]
			if bottom_cell.visited == False:
				potentials.append(bottom_cell)


		if len(potentials) != 0:
			random_choice = random.randint(0, (len(potentials)-1))
			choice = potentials[random_choice]
			return choice
		else:
			return 0	

	def RemoveWall(self, wall):
		if wall == "r":
			self.right = False
		if wall == "t":
			self.top = False
		if wall == "b":
			self.bottom = False
		if wall == "l":
			self.left = False

		

	def show(self):
		if self.top:
			pygame.draw.line(DISPLAY, (255, 0, 255), (self.x * CELLSIZE, self.y * CELLSIZE), ((self.x + 1) * CELLSIZE, self.y * CELLSIZE), 1)

		if self.right:		
			pygame.draw.line(DISPLAY, (255, 0, 255), ((self.x + 1) * CELLSIZE, (self.y) * CELLSIZE), ((self.x + 1) * CELLSIZE, (self.y + 1) * CELLSIZE), 1)

		if self.bottom:		
			pygame.draw.line(DISPLAY, (255, 0, 255), ((self.x + 1) * CELLSIZE, (self.y + 1) * CELLSIZE), ((self.x + 1) * CELLSIZE, (self.y + 1) * CELLSIZE), 1)
		
		if self.left:
			pygame.draw.line(DISPLAY, (255, 0, 255), (self.x * CELLSIZE, self.y * CELLSIZE), (self.x * CELLSIZE, (self.y + 1) * CELLSIZE), 1)	

	def hilight(self):
		pygame.draw.rect(DISPLAY, (255, 0, 255), (self.x * CELLSIZE, self.y * CELLSIZE, CELLSIZE, CELLSIZE))
	def mark(self):
		pygame.draw.rect(DISPLAY, (19, 0, 255), (self.x * CELLSIZE, self.y * CELLSIZE, CELLSIZE, CELLSIZE))

thestack = []

for c in range(0, COLS):
	for r in range(0, ROWS): 
		cell = Cell(r, c)
		cells.append(cell)
cellindex = 22
current = cells[cellindex]
current.visited = True

while True:
	DISPLAY.fill(0)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
			sys.exit()

	for cell in cells:
		cell.show()
	current.visited = True
	current.hilight()

	# pick a random from neighbors
	next_cell = current.FindNeighbors()	
	if next_cell == 0:
		if len(thestack) > 0:
			next_cell = thestack.pop()
		else:
			raw_input("Press Enter to continue...")
			sys.exit()

	else:	
	# push current on stack
		thestack.append(current)


	# remove walls
	if next_cell.x > current.x:
		current.RemoveWall("r")
		next_cell.RemoveWall("l")
	if next_cell.x < current.x:
		current.RemoveWall("l")
		next_cell.RemoveWall("r")
	if next_cell.y < current.y:
		current.RemoveWall("t")
		next_cell.RemoveWall("b")
	if next_cell.y > current.y:
		current.RemoveWall("b")
		next_cell.RemoveWall("t")

	# make next the current
	current = next_cell

	# mark current as visited
	current.visited = True

	# if stack is not empty
	# pop a cell from stack

	#make it current


	pygame.display.update()
	clock.tick(FPS)