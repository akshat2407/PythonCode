import pygame
import random
import time
import os
pygame.font.init()

WIDTH = 610
HEIGHT = 610
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ROWS, COLS = 4, 4
SQUARE_SIZE = 150
BACKGROUND = (196,183,169)
BOARD = [[0,0,0,0], 
		 [0,0,0,0], 
		 [0,0,0,0], 
		 [0,0,0,0]] 
COLORS = {0:(203,194,179),
		  2:(236,229,217),
		  4:(235,223,199),
		  8:(241,189,145),
		  16:(243,166,127),
		  32:(243,152,133),
		  64:(244,96,66),
		  128:(235,210,131),
		  256:(236,203,103),
		  512:(235,200,90),
		  1024:(231,194,87),
		  2048:(231,190,78)}
FONT = pygame.font.SysFont("comicsans", 60)
FONT_1 = pygame.font.Font(None, 60) 
l = []
COUNT = 0
temp_row = 0
temp_col = 0
highscore = 0
score = 0
logo = pygame.image.load(r'C:\Users\X1\Desktop\python\2048\logo.png')
logo = pygame.transform.scale(logo, (150, 150))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
pygame.display.update()


def main():
	global score
	score = 0
	print("main..")
	run = True
	CHECK = True
	gen_new_num()

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if CHECK:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						move_up()
					if event.key == pygame.K_DOWN:
						move_down()
					if event.key == pygame.K_LEFT:
						move_left()
					if event.key == pygame.K_RIGHT:
						move_right()


def draw_squares(win):
	win.fill(BACKGROUND)

	col = 0
	while(col < 4):
		row = 0
		while(row < 4):
			x = COLORS.get(BOARD[row][col])
			pygame.draw.rect(win, x, pygame.Rect(10+(140*col)+(10*col), 10+(140*row)+(10*row), 140, 140))
			if row == temp_row and col == temp_col:
				x = COLORS.get(0)
				pygame.draw.rect(win, x, pygame.Rect(10+(140*col)+(10*col), 10+(140*row)+(10*row), 140, 140))
			elif BOARD[row][col] != 0:
				text = FONT.render(str(BOARD[row][col]), 1, BLACK)
				if BOARD[row][col] > 10 and BOARD[row][col] < 100:
					win.blit(text, (55+(150*col), 75+(150*row)))
				elif BOARD[row][col] > 100 and BOARD[row][col] < 1000:
					win.blit(text, (40+(150*col), 75+(150*row)))
				elif BOARD[row][col] > 1000:
					win.blit(text, (25+(150*col), 75+(150*row)))
				else:
					win.blit(text, (75+(150*col), 75+(150*row)))
			row += 1
		col += 1
	pygame.display.update()

	time.sleep(0.5)
	x = COLORS.get(BOARD[temp_row][temp_col])
	pygame.draw.rect(win, x, pygame.Rect(10+(140*temp_col)+(10*temp_col), 10+(140*temp_row)+(10*temp_row), 140, 140))
	text = FONT.render(str(BOARD[temp_row][temp_col]), 1, BLACK)
	win.blit(text, (75+(150*temp_col), 75+(150*temp_row)))
	pygame.display.update()

	check_loss(win)

def gen_new_num():
	global COUNT, temp_col, temp_row
	COUNT += 1
	x = [2,4,8]

	num = random.choice(x)
	if num == 4 and COUNT % 2 != 0:
		num = 4
	elif num == 8 and COUNT % 6 == 0:
		num = 8
	else:
		num = 2

	row = random.randint(0, 3)
	col = random.randint(0, 3)
	while(BOARD[row][col] != 0):
		row = random.randint(0, 3)
		col = random.randint(0, 3)

	temp_row = row
	temp_col = col

	BOARD[row][col] = num

	draw_squares(WIN)

def move_down():
	col = 0
	while(col < 4):
		row = 0
		while(row < 4):
			if BOARD[row][col] != 0:
				l.append(BOARD[row][col])
			row += 1
		length = len(l) - 1

		movement(l, 'down')

		row = 3
		length = len(l) - 1
		while(length >= 0):
			BOARD[row][col] = l[length]
			row -= 1
			length -= 1

		l.clear()
		col += 1

	gen_new_num()

def move_up():
	col = 0
	while(col < 4):
		row = 0
		while(row < 4):
			if BOARD[row][col] != 0:
				l.append(BOARD[row][col])
			row += 1
		length = len(l) - 1

		movement(l, 'up')

		row = 0
		var = 0
		length = len(l) - 1
		while(var <= length):
			BOARD[row][col] = l[var]
			row += 1
			var += 1

		l.clear()
		col += 1

	gen_new_num()

def move_left():
	row = 0
	while(row < 4):
		col = 0
		while(col < 4):
			if BOARD[row][col] != 0:
				l.append(BOARD[row][col])
			col += 1
		length = len(l) - 1

		movement(l, 'left')

		col = 0
		var = 0
		length = len(l) - 1
		while(var <= length):
			BOARD[row][col] = l[var]
			col += 1
			var += 1

		l.clear()
		row += 1

	gen_new_num()

def move_right():
	row = 0
	while(row < 4):
		col = 0
		while(col < 4):
			if BOARD[row][col] != 0:
				l.append(BOARD[row][col])
			col += 1
		length = len(l) - 1

		movement(l, 'right')

		col = 3
		length = len(l) - 1
		while(length >= 0):
			BOARD[row][col] = l[length]
			col -= 1
			length -= 1

		l.clear()
		row += 1

	gen_new_num()

def check_loss(win):
	global CHECK, score, highscore
	col = 0
	x = 0
	while(col < 4):
		row = 0
		while(row < 4):
			if BOARD[row][col] == 0:
				x += 1
			row += 1
		col += 1

	if x == 0:
		CHECK = False
		text = FONT_1.render('Game Over', 1, RED)
		win.blit(text, (200, 275))
		text = FONT_1.render('Press Spacebar to restart', 1, RED)
		win.blit(text, (55, 315))
		pygame.display.update()

		col = 0
		while(col < 4):
			row = 0
			while(row < 4):
				if BOARD[row][col] > score:
					score = BOARD[row][col]
				row += 1
			col += 1

		if score > highscore:
			highscore = score

		restart()

def movement(l, move):
	index = len(l) - 1
	while(index > 0):
		if l[index] == l[index - 1]:
			l[index - 1] = l[index] + l[index - 1]
			l.pop(index)
			index -= 1
		index -= 1

	index = 0
	for index in range(0, len(l)):
		if l[index] == 0:
			l.pop(index)

	append_0 = 4 - len(l)

	while(append_0 > 0):
		if move == 'up' or move == 'left':
			l.append(0)
		else:
			l.insert(0,0)
		append_0 -= 1

	return l


def restart():
	global BOARD
	run = True
	while(run):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					BOARD = [[0,0,0,0], 
							[0,0,0,0], 
							[0,0,0,0], 
							[0,0,0,0]]
					run = False
					pygame.display.update()
					menu_screen(WIN)


def menu_screen(win):
	win.fill(BACKGROUND)
	r = True
	text = FONT_1.render('Click to Play!!', 1, BLACK)
	win.blit(text, (150, 450))
	text = FONT.render('Highscore: ', 1, RED)
	win.blit(text, (150, 250))
	text = FONT.render('Score: ', 1, RED)
	win.blit(text, (150, 350))
	text = FONT.render(str(highscore), 1, RED)
	win.blit(text, (400, 250))
	text = FONT.render(str(score), 1, RED)
	win.blit(text, (400, 350))
	win.blit(logo, (240, 50))
	pygame.display.update()
	while(r):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				r = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.display.update()
				main()



menu_screen(WIN)