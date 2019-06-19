from tkinter import *
import time, random
debug = 0
width = 360
rotation = 0
spx = width/2
spy = 0
blocks_in_row = 12
te = width/blocks_in_row
height = width * 2-6*te
root = Tk()
block_type = "n"
delay =1500
base_delay = 1500
score = 0
first_time = True
root.title("TkTris")
f = Canvas(root, width=width, height=height)
helpg = 0
f.pack()
def toggle_grid(event):
	global helpg
	if helpg:
		helpg = 0
		f.delete("grid")
	else:
		helpg = 1
		grid()
		
def grid():
	global helpg
	if helpg: 
		for i in range(blocks_in_row):
			f.create_line(i*te, 0, i*te, height, tags="grid")
		for i in range(int(height/te)):
			f.create_line(0, i*te, width, i*te, tags="grid")
def evoke_rotate_cw(event):
	global first_time
	first_time = True
	rotate_cw(block_type, rotation)

def evoke_rotate_ccw(event):
	global first_time
	first_time = True
	rotate_ccw(block_type, rotation)

def check_wall_right():
	if f.coords("a")[2] < width and f.coords("b")[2] < width and  f.coords("c")[2] < width and  f.coords("d")[2] < width:
		return True
	else:
		return False
def check_rotate_right():
	if f.coords("a")[2] -1 < width and f.coords("b")[2] - 1 < width and  f.coords("c")[2] - 1 < width and  f.coords("d")[2] - 1 < width:
		return True
	else:
		return False
def check_wall_left():
	if f.coords("a")[0] > 0 and f.coords("b")[0] > 0 and  f.coords("c")[0] > 0 and  f.coords("d")[0] > 0:
		return True
	else:
		return False
		return False
def check_rotate_left():
	if f.coords("a")[0] + 1> 0 and f.coords("b")[0] + 1 > 0 and  f.coords("c")[0] + 1 > 0 and  f.coords("d")[0] + 1 > 0:
		return True
	else:
		return False
def check_wall_down():
	if f.coords("a")[3] < height and f.coords("b")[3] < height and  f.coords("c")[3] < height and  f.coords("d")[3] < height:
		return True
	else:
		return False
def block_fall():
	#print(f.coords("a"))
	#print(f.coords("b"))
#	print(f.coords("c"))
#	print(f.coords("d"))
	try:
		if check_wall_down():
			f.move("block", 0, te)
			if colisioncheck():
				f.move("block", 0, -te)
				fallen()
		else:
			fallen()
	except IndexError:
		if debug:
			print("spawning")
		pass
def colisioncheck():
	touch = f.find_overlapping(f.coords("a")[0]+3,f.coords("a")[1]+3, f.coords("a")[2]-3, f.coords("a")[3]-3 ) + f.find_overlapping(f.coords("b")[0]+3,f.coords("b")[1]+3, f.coords("b")[2]-3, f.coords("b")[3]-3 ) + f.find_overlapping(f.coords("c")[0]+3,f.coords("c")[1]+3, f.coords("c")[2]-3, f.coords("c")[3]-3 ) + f.find_overlapping(f.coords("d")[0]+3,f.coords("d")[1]+3, f.coords("d")[2]-3, f.coords("d")[3]-3 )
	
	
	block_pieces = f.find_withtag("block")
	colided = False
	for i in touch:
		if i not in block_pieces:
			colided = True
			if debug:
				print("colided")
			break

	return colided 	
def reset(event):
	fallen()
	global delay
	global base_delay
	delay = base_delay
	f.delete(ALL)
	print(score)
	if helpg:
		grid()
def loop():
	global delay
	global base_delay
	if delay > 250:
		delay = int(base_delay - score/2)
		if debug:
			print("delay:"+ str(delay))
	block_fall()
	spawn()
	root.after(delay, loop)
def scan_line():
	i = 1
	global score
	f.delete("grid")
	for j in range(5):
		while i < (int(height/te)):
			scaner = f.find_overlapping(0, height-int(i*te)+5, width, height-int(i*te)+5)
			if scaner == ():
				break


			if len(scaner) > blocks_in_row-1:
				for l in scaner:
					f.delete(l)
				leftovers = f.find_overlapping(0, 0, width, height-int(i*te)+5)	
				for k in leftovers:
					f.move(k, 0, te)
				i = 0
				score += 100
			scaner = ()
			i += 1
	grid()
def block_left(event):
	if check_wall_left():
		f.move("block", -te, 0)
		if colisioncheck():
			f.move("block", te, 0)

def block_right(event):
	if check_wall_right():
		f.move("block", te, 0)
		if colisioncheck():
			f.move("block", -te, 0)


def block_down(event):
	if check_wall_down():

		f.move("block", 0, te)
		if colisioncheck():
			f.move("block", 0, -te)
			fallen()
		
	else:
		fallen()

def block_harddrop(event):
	while check_wall_down() and not colisioncheck():
		f.move("block", 0, te)
	if colisioncheck():
		f.move("block", 0, -te)
	fallen()
def rotate_cw(x, y):
	global rotation
	global first_time
	if x == "i":
		if y == 0:
			f.move("b", te, -te )
			f.move("c", -te, te)
			f.move("d", -2*te, 2*te) 
			rotation = 1
		if y == 1:
			f.move("b", -te, te )
			f.move("c", te, -te)
			f.move("d", 2*te, -2*te) 
			rotation = 0
	if x == "o":
		pass
	if x == "s":
		if y == 0:
			f.move("c", te, -2*te)
			f.move("d", te, 0)
			rotation = 1
			
		if y == 1:
			f.move("c", -te, 2*te)
			f.move("d", -te, 0)
			rotation = 0

	if x == "z":
		if y == 0:
			f.move("b", te, 2*te)
			f.move("a", te, 0)
			rotation = 1
			
		if y == 1:
			f.move("b", -te, -2*te)
			f.move("a", -te, 0)
			rotation = 0	
	if x == "l":
		if y == 0:
			f.move("b", 2*te, 0)
			f.move("c", 0, te)
			f.move("a", te, -te)
			f.move("d", te, -2*te)
			

			rotation = 3
		if y == 1:
			f.move("c", 2*te, te)
			f.move("a", 0, -te)

			rotation = 0
		if y == 2:

			f.move("b", -2*te, 0)
			f.move("c", -2*te, -2*te)

			rotation = 1
		if y == 3:

			f.move("a", -te, 2*te)
			f.move("d", -te, 2*te)
			rotation = 2		
	if x == "j":
		if y == 0:
			f.move("b", 2*te, -te)
			f.move("a", 0, te)
			rotation = 1
		if y == 1:
			f.move("c", -2*te, te)
			f.move("b", -2*te, te)
			rotation = 2
		if y == 2:
			f.move("a", -te, -2*te)
			f.move("d", -te, -2*te)
			rotation = 3
		if y == 3:
			f.move("b", -2*te, -te)
			f.move("c", 0, -2*te)
			f.move("a", -te, 0)
			f.move("d", -te, te)
			rotation = 0					
	if x == "t":
		if y == 0:
			f.move("b", te, -te)
			f.move("c", -te, te)
			f.move("d", -te, -te)
			rotation = 1
		if y == 1:
			f.move("b", te, te)
			f.move("c", -te, -te)
			f.move("d", te, -te)
			rotation = 2
		if y == 2:
			f.move("b", -te, te)
			f.move("c", te, -te)
			f.move("d", te, te)
			rotation = 3
		if y == 3:
			f.move("b", -te, -te)
			f.move("c", te, te)
			f.move("d", -te, te)
			rotation = 0
	if debug:		
		print(rotation)
	if first_time == True:
		if not check_wall_down() or not check_rotate_left() or not check_rotate_right() or colisioncheck():
			first_time = False
			rotate_ccw(block_type, rotation)
def rotate_ccw(x, y):
	global rotation
	global first_time
	if x == "i":
		if y == 0:
			f.move("b", te, -te )
			f.move("c", -te, te)
			f.move("d", -2*te, 2*te) 
			rotation = 1
		if y == 1:
			f.move("b", -te, te )
			f.move("c", te, -te)
			f.move("d", 2*te, -2*te) 
			rotation = 0
	if x == "o":
		pass
	if x == "s":
		if y == 0:
			f.move("c", te, -2*te)
			f.move("d", te, 0)
			rotation = 1
			
		if y == 1:
			f.move("c", -te, 2*te)
			f.move("d", -te, 0)
			rotation = 0

	if x == "z":
		if y == 0:
			f.move("b", te, 2*te)
			f.move("a", te, 0)
			rotation = 1
			
		if y == 1:
			f.move("b", -te, -2*te)
			f.move("a", -te, 0)
			rotation = 0			
	if x == "l":
		if y == 0:
			f.move("c", -2*te, -te)
			f.move("a", 0, te)
			rotation = 1
		if y == 1:
			f.move("b", 2*te, 0)
			f.move("c", 2*te, 2*te)
			rotation = 2
		if y == 2:
			f.move("a", te, -2*te)
			f.move("d", te, -2*te)
			rotation = 3
		if y == 3:
			f.move("b", -2*te, 0)
			f.move("c", 0, -te)
			f.move("a", -te, te)
			f.move("d", -te, 2*te)
			rotation = 0

	if x == "j":
		if y == 0:
			f.move("b", 2*te, te)
			f.move("c", 0, 2*te)
			f.move("a", te, 0)
			f.move("d", te, -te)
			

			rotation = 3
		if y == 1:
			f.move("b", -2*te, te)
			f.move("a", 0, -te)			

			rotation = 0
		if y == 2:

			f.move("c", 2*te, -te)
			f.move("b", 2*te, -te)			
	

			rotation = 1
		if y == 3:
			f.move("a", te, 2*te)
			f.move("d", te, 2*te)
			rotation = 2					
	if x == "t":
		if y == 0:
			f.move("b", te, te)
			f.move("c", -te, -te)
			f.move("d", te, -te)


			rotation = 3
		if y == 1:
			f.move("b", -te, te)
			f.move("c", te, -te)
			f.move("d", te, te)

			rotation = 0
		if y == 2:

			f.move("b", -te, -te)
			f.move("c", te, te)
			f.move("d", -te, te)


			rotation = 1
		if y == 3:
			f.move("b", te, -te)
			f.move("c", -te, te)
			f.move("d", -te, -te)
			rotation = 2
	if debug:
		print(rotation)
	if first_time == True:
		if not check_wall_down() or not check_rotate_left() or not check_rotate_right() or colisioncheck():
			first_time = False
			rotate_cw(block_type, rotation)
			
def spawn():
	i = random.randint(1,7)


	if block_type == "n":
		cnt = 0
		if i == 1:
			spawn_t()
		elif i == 2:
			spawn_o()
		elif i == 3:
			spawn_i()
		elif i == 4:
			spawn_l()
		elif i == 5:
			spawn_j()
		elif i == 6:
			spawn_s()
		elif i == 7:
			spawn_z()
		if debug:	
			print(block_type)
		if cnt < 2 and colisioncheck():
			print("You scored: " + str(score))
			fallen()
			f.delete(ALL)

		else:
			cnt += 1
def spawn_t():
	f.delete("block")
	global block_type
	block_type = "t"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="purple", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="purple", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="purple", tags=("block", "c") )
	f.move(tile3, te, 0)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="purple", tags=("block", "d") )
	f.move(tile4, 0, te)
	
def spawn_l():
	f.delete("block")
	global block_type
	block_type = "l"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue", tags=("block", "c") )
	f.move(tile3, te, 0)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue", tags=("block", "d") )
	f.move(tile4, -te, te)
	
def spawn_j():
	f.delete("block")
	global block_type
	block_type = "j"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange", tags=("block", "c") )
	f.move(tile3, te, 0)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange", tags=("block", "d") )
	f.move(tile4, te, te)
	
def spawn_o():
	f.delete("block")
	global block_type
	block_type = "o"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow", tags=("block", "c") )
	f.move(tile3, 0, te)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow", tags=("block", "d") )
	f.move(tile4, -te, te)
	
def spawn_i():
	f.delete("block")
	global block_type
	block_type = "i"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan", tags=("block", "b" ))
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan", tags=("block", "c") )
	f.move(tile3, te, 0)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan", tags=("block", "d"))
	f.move(tile4, 2*te, 0)
def spawn_s():
	f.delete("block")
	global block_type
	block_type = "s"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green", tags=("block", "c") )
	f.move(tile3, -2*te, te)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green", tags=("block", "d") )
	f.move(tile4, -te, te)
	
def spawn_z():
	f.delete("block")
	global block_type
	block_type = "z"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red", tags=("block", "c") )
	f.move(tile3, 0, te)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red", tags=("block", "d") )
	f.move(tile4, te, te)
	

def fallen():
	#print(f.coords("a"))
	#print(f.coords("b"))
	#print(f.coords("c"))
	#print(f.coords("d"))
	
	f.create_rectangle(f.coords("a"), tags="brick", fill="black")
	f.create_rectangle(f.coords("b"), tags="brick", fill="black")
	f.create_rectangle(f.coords("c"), tags="brick", fill="black")
	f.create_rectangle(f.coords("d"), tags="brick", fill="black")
	f.delete("block")
	global block_type
	block_type = "n"
	global rotation
	rotation = 0
	scan_line()
root.bind("e", evoke_rotate_cw)
root.bind("q", evoke_rotate_ccw)
root.bind("a", block_left)
root.bind("d", block_right)
root.bind("s", block_down)
root.bind("w", block_harddrop)
root.bind("g", toggle_grid)
root.bind("r", reset)
root.after(delay, loop)
root.mainloop()
