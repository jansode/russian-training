import settings
import random
import time
import os

TETRIS_WIDTH = 10
TETRIS_HEIGHT = 20
tetris_grid = '.'*TETRIS_WIDTH*TETRIS_HEIGHT

piece_I = [["#####"],["#","#","#","#"]]
piece_O = [["##","##"]]
piece_J = [["###","..#"],[".#",".#","##"]]
piece_L = [["###","#.."],["#.","#.","##"]]
piece_T = [["###",".#."],["#","##","#"],[".#.","###"],[".#","##",".#"]]
piece_S = [[".##","##"],["#.","##",".#"]]
piece_Z = [["##",".##"],[".#","##","#."]]

pieces = [piece_I,piece_O,piece_J,piece_L,piece_T,piece_S,piece_Z]
locked_indices = []


def replace_str_at_index(s,insert,index):
	return s[:index] + insert + s[index+len(insert):]
	
def draw_piece(piece,x,y):
	global tetris_grid

	for i,layer in enumerate(piece):
		tetris_grid = replace_str_at_index(tetris_grid,layer,(y+i)*TETRIS_WIDTH+x)

def draw_locked_indices():
	global tetris_grid
	global locked_indices
	
	for index in locked_indices:
		tetris_grid = replace_str_at_index(tetris_grid,"#",index[1]*TETRIS_WIDTH+index[0])

def check_collision(x,y,piece):
	global locked_indices
	
	print("check_collision piece:")
	print(piece)
	
	piece_coordinates = []
	
	for y_i in range(len(piece)):
		for x_i in range(len(piece[y_i])):
			if piece[y_i][x_i] == '#':
				piece_coordinates.append((x+x_i,y+y_i))
	
	print("piece coordinates:")
	print(piece_coordinates)
	for index in locked_indices:
		for c in piece_coordinates:
			test_coord = (c[0],c[1]+1)
			if test_coord == index:
				return True
	
	return False
		
def clear_board_at(index,size):
	global tetris_grid
	tetris_grid = replace_str_at_index(tetris_grid,"."*size,index)

def clear_board():
	global tetris_grid
	tetris_grid = '.'*TETRIS_WIDTH*TETRIS_HEIGHT
		
def print_tetris_board():
	for y in range(TETRIS_HEIGHT):
		for x in range(TETRIS_WIDTH):
			print(tetris_grid[y*TETRIS_WIDTH+x],end='',flush=True)
		print(flush=True)

def handle_line_clearing():
	global locked_indices
	global tetris_grid
	
	full_lines_y = []
	for y in range(TETRIS_HEIGHT):
		line_full = True
		for x in range(TETRIS_WIDTH):
			if tetris_grid[y*TETRIS_WIDTH+x] != '#':
				line_full = False
		
		if line_full:
			full_lines_y.append(y)
	
	to_remove = []
	for c in locked_indices:
		for line_y in full_lines_y:
			if c[1] == line_y:
				to_remove.append(c)
	
	for i in to_remove:
		locked_indices.remove(i)

def handle_collisions(current_piece,current_piece_location,current_piece_rotation):
	global tetris_grid
	global locked_indices

	# check collision with floor
	if current_piece_location[1] + len(pieces[current_piece][current_piece_rotation]) == TETRIS_HEIGHT:	
		locked_indices = []
		for y in range(TETRIS_HEIGHT):
			for x in range(TETRIS_WIDTH):
				if tetris_grid[y*TETRIS_WIDTH+x] == "#":
					locked_indices.append((x,y))
					
		handle_line_clearing()
		return True
		

	
	# check collision with occupied squares
	if check_collision(current_piece_location[0],current_piece_location[1], pieces[current_piece][current_piece_rotation]):
		print("COLLITION")
		
		locked_indices = []
		for y in range(TETRIS_HEIGHT):
			for x in range(TETRIS_WIDTH):
				if tetris_grid[y*TETRIS_WIDTH+x] == "#":
					locked_indices.append((x,y))
			
		handle_line_clearing()
		return True
	return False
	
def handle_gravity():
	global tetris_grid
	global locked_indices
	'''
	for y in range(TETRIS_HEIGHT):
		for x in range(TETRIS_WIDTH):
	'''	

def get_piece_size_y(piece):
	return len(piece)
	
def get_piece_size_x(piece):
	return len(pieces[0])
	
import keyboard
def start_tetris():
	global locked_indices

	locked_indices = []
	settings.PLAYING_TETRIS = True
	
	current_piece = random.randint(0,len(pieces)-1)
	current_piece_location = (3,0)
	current_piece_rotation = 0
	
	while True:
		if current_piece_location == (3,0) and check_collision(current_piece_location[0],current_piece_location[1],pieces[current_piece][current_piece_rotation]):
			print("GAME OVER!")
			break
			
		if current_piece_location[1]+get_piece_size_y(pieces[current_piece][current_piece_rotation]) >= TETRIS_HEIGHT:
			current_piece_location = (current_piece_location[0],TETRIS_HEIGHT)
		if current_piece_location[0] <= 0:
			current_piece_location = (0,current_piece_location[1])
		if current_piece_location[0]+get_piece_size_x(pieces[current_piece][current_piece_rotation]) >= TETRIS_WIDTH:
			current_piece_location = (TETRIS_WIDTH,current_piece_location[1])

		print("Locked indices:")
		for locked in locked_indices:
			print(locked,end="")
		
		if keyboard.is_pressed('up'):
			current_piece_rotation = (current_piece_rotation+1) % len(pieces[current_piece])
		if keyboard.is_pressed('left'):
			current_piece_location = (current_piece_location[0]-1,current_piece_location[1])
		if keyboard.is_pressed('right'):
			current_piece_location = (current_piece_location[0]+1,current_piece_location[1])
		if keyboard.is_pressed('down'):
			current_piece_location = (current_piece_location[0],current_piece_location[1]+1)
		if keyboard.is_pressed('x'):
			break
		
		draw_piece(pieces[current_piece][current_piece_rotation],current_piece_location[0],current_piece_location[1])
		draw_locked_indices()
		print_tetris_board()
		
		print("Press X to exit")
		
		if handle_collisions(current_piece,current_piece_location,current_piece_rotation):	
			current_piece = random.randint(0,len(pieces)-1)
			current_piece_location = (3,0)
			current_piece_rotation = 0
			os.system("cls")
			continue

		time.sleep(0.2)
		os.system("cls")
		current_piece_location = (current_piece_location[0],current_piece_location[1]+1)
		clear_board()
		