#!/bin/python3
from tkinter import *
import time, random, os
playername = os.getlogin()
print(playername)
alph = ["a", "b", "c", "d"]

minimal_delay = 250
delay = 1500
base_delay = 1500

debug = 0
width = 360
rotation = 0
spx = width/2
spy = 0
blocks_in_row = 12
te = width/blocks_in_row
height = width * 2-6*te
root = Tk()
root.configure(background="gray20")
block_type = "n"

score = 0
first_time = True
root.title("TkTris")
frame = Frame(root)
frame.configure(background="gray20")
sbframe = Frame(frame)
sbframe.configure(background="gray20")
hold_blocker = False
f = Canvas(frame, width=width, height=height, bg="black")
pv = Canvas(frame, width=te*4, height= te*3, bg="black")
l1 = Label(frame, text="Next up:")
l2 = Label(frame, text="hold")
l3 = Label(frame, text="Your score:")
scr = StringVar()
lscore = Label(frame, textvariable=scr)
darken = [l1, l2, l3, lscore]
for d in darken:
	d.configure(background="gray20", foreground="white")

holdpv = Canvas(frame, width=te*4, height= te*3, bg="black")
helpg = 0
frame.pack()
f.pack(side="left")
l1.pack()
pv.pack()
l2.pack()
holdpv.pack()

l3.pack()
lscore.pack()
sbframe.pack()
holder = "n"
permholder = "n"
itemcolor = "gray"
nextup = random.randint(1,7)
bag = [1,2,3,4,5,6,7]
pause = False

class ScoreBoard:
	def __init__(self,root):
		for i in range(4):
			for j in range(2):
				self.e = Entry(root, width=int(te/4))
				self.e.grid(row=i, column=j)
				try:
					self.e.insert(END, scores[i][j])
				except IndexError:
					#self.e.insert(END, "null")
					pass
				self.e.config(state="disabled",disabledbackground="gray25", disabledforeground="white")




def readScores():
	global scores
	global sb
	scores = []
	try:
		with open("scores.dat") as file:
			lines = file.readlines()
			for line in lines:
				scores.append(line.strip().split(", "))
			print(scores)
			sb = ScoreBoard(sbframe)
			file.close()
	except FileNotFoundError:
		print("Error, scores.dat is missing")
		os.system(">scores.dat")
		readScores()


def toggle_pause(event):
		global pause
		pause = not pause

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
			f.create_line(i*te, 0, i*te, height, tags="grid", fill=itemcolor)
		for i in range(int(height/te)):
			f.create_line(0, i*te, width, i*te, tags="grid", fill=itemcolor)
def evoke_rotate_cw(event):
	global first_time
	first_time = True
	rotate_cw(block_type, rotation)

def evoke_rotate_ccw(event):
	global first_time
	first_time = True
	rotate_ccw(block_type, rotation)

def check_wall_right():
	if f.coords("a")[2] < width and f.coords("b")[2] < width and  f.coords("c")[2] < width and	f.coords("d")[2] < width:
		return True
	else:
		return False
def check_rotate_right():
	if f.coords("a")[2] -1 < width and f.coords("b")[2] - 1 < width and	 f.coords("c")[2] - 1 < width and  f.coords("d")[2] - 1 < width:
		return True
	else:
		return False
def check_wall_left():
	if f.coords("a")[0] > 0 and f.coords("b")[0] > 0 and  f.coords("c")[0] > 0 and	f.coords("d")[0] > 0:
		return True
	else:
		return False
		return False
def check_rotate_left():
	if f.coords("a")[0] + 1> 0 and f.coords("b")[0] + 1 > 0 and	 f.coords("c")[0] + 1 > 0 and  f.coords("d")[0] + 1 > 0:
		return True
	else:
		return False
def check_wall_down():
	if f.coords("a")[3] < height and f.coords("b")[3] < height and	f.coords("c")[3] < height and  f.coords("d")[3] < height:
		return True
	else:
		return False
		
def gcheck_wall_down():
	if f.coords("ga")[3] < height and f.coords("gb")[3] < height and	f.coords("gc")[3] < height and  f.coords("gd")[3] < height:
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
	ghost_drop()
	
	
def ghost_drop():
	f.coords("ga", f.coords("a"))
	f.coords("gb", f.coords("b"))
	f.coords("gc", f.coords("c"))
	f.coords("gd", f.coords("d"))
	try:
		while gcheck_wall_down():
			f.move("ghost", 0, te)
			if gcolisioncheck():
				f.move("ghost", 0, -te)
				break
		
	except IndexError:
		if debug:
			print("gspawning")
		pass
	f.tag_lower("ghost")
def colisioncheck():
	touch = f.find_overlapping(f.coords("a")[0]+3,f.coords("a")[1]+3, f.coords("a")[2]-3, f.coords("a")[3]-3 ) + f.find_overlapping(f.coords("b")[0]+3,f.coords("b")[1]+3, f.coords("b")[2]-3, f.coords("b")[3]-3 ) + f.find_overlapping(f.coords("c")[0]+3,f.coords("c")[1]+3, f.coords("c")[2]-3, f.coords("c")[3]-3 ) + f.find_overlapping(f.coords("d")[0]+3,f.coords("d")[1]+3, f.coords("d")[2]-3, f.coords("d")[3]-3 )


	block_pieces = f.find_withtag("block")
	ghost_pieces = f.find_withtag("ghost")
	colided = False
	for i in touch:
		if i not in block_pieces and i not in ghost_pieces:
			colided = True
			if debug:
				print("colided")
			break

	return colided
def gcolisioncheck():
	touch = f.find_overlapping(f.coords("ga")[0]+3,f.coords("ga")[1]+3, f.coords("ga")[2]-3, f.coords("ga")[3]-3 ) + f.find_overlapping(f.coords("gb")[0]+3,f.coords("gb")[1]+3, f.coords("gb")[2]-3, f.coords("gb")[3]-3 ) + f.find_overlapping(f.coords("gc")[0]+3,f.coords("gc")[1]+3, f.coords("gc")[2]-3, f.coords("gc")[3]-3 ) + f.find_overlapping(f.coords("gd")[0]+3,f.coords("gd")[1]+3, f.coords("gd")[2]-3, f.coords("gd")[3]-3 )

	block_pieces = f.find_withtag("block")
	ghost_pieces = f.find_withtag("ghost")
	colided = False
	for i in touch:
		if i not in ghost_pieces and i not in block_pieces:
			colided = True
			if debug:
				print("ghostcolided")
			break

	return colided
def reset(event):
	fallen()
	global score
	global delay
	global base_delay
	delay = base_delay
	global permholder
	permholder = "n"
	global holder
	holder = "n"
	pv.delete(ALL)
	holdpv.delete("block")
	f.delete(ALL)
	print(score)
	score = 0
	if helpg:
		grid()
def loop():
	global delay
	global base_delay
	global scr
	scr.set(str(score))
	print(score)
	if delay > minimal_delay:
		delay = int(base_delay - score/4)
	if not pause:
		block_fall()
		if debug:
			print("delay:"+ str(delay))
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
	ghost_drop()
	
def block_right(event):
	if check_wall_right():
		f.move("block", te, 0)
		if colisioncheck():
			f.move("block", -te, 0)
	ghost_drop()

def block_down(event):
	if check_wall_down():

		f.move("block", 0, te)
		if colisioncheck():
			f.move("block", 0, -te)
			fallen()

	else:
		fallen()
	ghost_drop()
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
	ghost_drop()
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
	ghost_drop()


def randomPiece():
	global bag
	r = random.randint(0,len(bag)-1)
	out = bag[r]
	bag.remove(out)
	if not len(bag):
		bag = [1,2,3,4,5,6,7]
	return out
def hold(event):
	global permholder
	
	global rotation
	global block_type
	global hold_blocker
	if not hold_blocker:
		hold_blocker = True
		holder = permholder
		permholder = block_type
		
		rotation = 0
		if permholder == "t":
			hold_t()
		elif permholder == "o":
			hold_o()
		elif permholder == "i":
			hold_i()
		elif permholder =="l":
			hold_l()
		elif permholder == "j":
			hold_j()
		elif permholder == "s":
			hold_s()
		elif permholder == "z":
			hold_z()
		if holder == "t":
			spawn_t()

		elif holder == "o":
			spawn_o()

		elif holder == "i":
			spawn_i()

		elif holder == "l":
			spawn_l()

		elif holder == "j":
			spawn_j()

		elif holder == "s":
			spawn_s()

		elif holder == "z":
			spawn_z()
		elif holder == "n":
			print("holder == n")
			block_type = "n"
			spawn()
		for i in alph:
			try:
				f.itemconfig("g"+i, fill=f.itemcget(i, "fill")+"4")
			except TclError:
				f.itemconfig("g"+i, fill=f.itemcget(i, "fill")[:-1]+"4")
		ghost_drop()
def spawn():



	if block_type == "n":
		global nextup
		global delay
		i = nextup
		nextup = randomPiece()
		cnt = 0
		if i == 1:
			spawn_t()
			gspawn_t()
		elif i == 2:
			spawn_o()
			gspawn_o()	

		elif i == 3:
			spawn_i()
			gspawn_i()
		elif i == 4:
			spawn_l()
			gspawn_l()

		elif i == 5:
			spawn_j()
			gspawn_j()

		elif i == 6:
			spawn_s()
			gspawn_s()

		elif i == 7:
			spawn_z()
			gspawn_z()
		ghost_drop()
		if debug:
			print(block_type)
		if cnt < 2 and colisioncheck():
			global score, delay, base_delay

			print("You scored: " + str(score))
			global scores
			
			for i in range(len(scores)):
				try:
					if score > int(scores[i][1]):
						scores.insert(i, [playername, score])
						break
				except IndexError:
						scores[i] = [playername, score]
			if not len(scores):
				scores.append([playername, score])
			print(scores)
			writeScores()
			
			readScores()
			fallen()
			f.delete(ALL)
			holdpv.delete(ALL)
			pv.delete(ALL)
			global holder
			holder = "n"
			global permholder
			permholder = "n"
			global hold_blocker
			hold_blocker = 0
			score = 0
			delay = base_delay

		else:
			cnt += 1


		if nextup == 1:
			nextup_t()
		elif nextup == 2:
			nextup_o()
		elif nextup == 3:
			nextup_i()
		elif nextup == 4:
			nextup_l()
		elif nextup == 5:
			nextup_j()
		elif nextup == 6:
			nextup_s()
		elif nextup == 7:
			nextup_z()	


def writeScores():
	with open("scores.dat", "w") as file:
		for i in scores:
			file.write(str(i[0]))
			file.write(", ")
			file.write(str(i[1]))
			file.write("\n")
		file.close()

def spawn_t():
	f.delete("block")
	global block_type
	block_type = "t"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta1", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta1", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta1", tags=("block", "c") )
	f.move(tile3, te, 0)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta1", tags=("block", "d") )
	f.move(tile4, 0, te)
def nextup_t():
	pv.delete("block")

	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "c") )
	pv.move(tile3, te, 0)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "d") )
	pv.move(tile4, 0, te)
	
def hold_t():
	holdpv.delete("block")

	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "c") )
	holdpv.move(tile3, te, 0)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="magenta1", tags=("block", "d") )
	holdpv.move(tile4, 0, te)
	
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
	
def nextup_l():
	pv.delete("block")
	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "c") )
	pv.move(tile3, te, 0)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "d") )
	pv.move(tile4, -te, te)

def hold_l():
	holdpv.delete("block")
	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "c") )
	holdpv.move(tile3, te, 0)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="blue", tags=("block", "d") )
	holdpv.move(tile4, -te, te)

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

def nextup_j():
	pv.delete("block")

	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "c") )
	pv.move(tile3, te, 0)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "d") )
	pv.move(tile4, te, te)		  

def hold_j():
	holdpv.delete("block")

	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "c") )
	holdpv.move(tile3, te, 0)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="orange", tags=("block", "d") )
	holdpv.move(tile4, te, te)		  


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
	
def nextup_o():
	pv.delete("block")
	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "c") )
	pv.move(tile3, 0, te)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "d") )
	pv.move(tile4, -te, te)
	
def hold_o():
	holdpv.delete("block")
	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "c") )
	holdpv.move(tile3, 0, te)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="yellow", tags=("block", "d") )
	holdpv.move(tile4, -te, te)
	
	
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

def nextup_i():
	pv.delete("block")

	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "b" ))
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "c") )
	pv.move(tile3, te, 0)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "d"))
	pv.move(tile4, -2*te, 0)

def hold_i():
	holdpv.delete("block")

	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "b" ))
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "c") )
	holdpv.move(tile3, te, 0)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="cyan", tags=("block", "d"))
	holdpv.move(tile4, -2*te, 0)


def spawn_s():
	f.delete("block")
	global block_type
	block_type = "s"
	tile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green2", tags=("block", "a"))
	tile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green2", tags=("block", "b") )
	f.move(tile2, -te, 0)
	tile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green2", tags=("block", "c") )
	f.move(tile3, -2*te, te)
	tile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green2", tags=("block", "d") )
	f.move(tile4, -te, te)

def nextup_s():

	pv.delete("block")

	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "c") )
	pv.move(tile3, -2*te, te)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "d") )
	pv.move(tile4, -te, te)	
	
def hold_s():

	holdpv.delete("block")

	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "c") )
	holdpv.move(tile3, -2*te, te)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="green2", tags=("block", "d") )
	holdpv.move(tile4, -te, te)	
	
	   
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

def nextup_z():
	pv.delete("block")

	tile1 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "a"))
	tile2 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "b") )
	pv.move(tile2, -te, 0)
	tile3 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "c") )
	pv.move(tile3, 0, te)
	tile4 = pv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "d") )
	pv.move(tile4, te, te)

def hold_z():
	holdpv.delete("block")

	tile1 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "a"))
	tile2 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "b") )
	holdpv.move(tile2, -te, 0)
	tile3 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "c") )
	holdpv.move(tile3, 0, te)
	tile4 = holdpv.create_rectangle(2*te, te, 3*te,2*te, fill="red", tags=("block", "d") )
	holdpv.move(tile4, te, te)


def gspawn_t():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta4", tags=("ghost", "gc") )
	f.move(gtile3, te, 0)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="magenta4", tags=("ghost", "gd") )
	f.move(gtile4, 0, te)

def gspawn_l():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue4", tags=("ghost", "gc") )
	f.move(gtile3, te, 0)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="blue4", tags=("ghost", "gd") )
	f.move(gtile4, -te, te)

def gspawn_j():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange4", tags=("ghost", "gc") )
	f.move(gtile3, te, 0)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="orange4", tags=("ghost", "gd") )
	f.move(gtile4, te, te)


def gspawn_o():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow4", tags=("ghost", "gc") )
	f.move(gtile3, 0, te)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="yellow4", tags=("ghost", "gd") )
	f.move(gtile4, -te, te)
def gspawn_i():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan4", tags=("ghost", "gb" ))
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan4", tags=("ghost", "gc") )
	f.move(gtile3, te, 0)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="cyan4", tags=("ghost", "gd"))
	f.move(gtile4, 2*te, 0)

def gspawn_s():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green4", tags=("ghost", "gc") )
	f.move(gtile3, -2*te, te)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="green4", tags=("ghost", "gd") )
	f.move(gtile4, -te, te)


def gspawn_z():
	f.delete("ghost")

	gtile1 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red4", tags=("ghost", "ga"))
	gtile2 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red4", tags=("ghost", "gb") )
	f.move(gtile2, -te, 0)
	gtile3 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red4", tags=("ghost", "gc") )
	f.move(gtile3, 0, te)
	gtile4 = f.create_rectangle(spx, spy, spx + te, spy+ te, fill="red4", tags=("ghost", "gd") )
	f.move(gtile4, te, te)


def fallen():
	#print(f.coords("a"))
	#print(f.coords("b"))
	#print(f.coords("c"))
	#print(f.coords("d"))
	for i in alph:
		f.create_rectangle(f.coords(i), tags="brick", fill=f.itemcget(i, "fill"))
	
	f.delete("block")
	f.delete("ghost")
	global block_type
	block_type = "n"
	global rotation
	rotation = 0
	global hold_blocker
	hold_blocker = False
	scan_line()
	
#Controls
nextup = randomPiece()
readScores()
root.bind("e", evoke_rotate_cw)
root.bind("q", evoke_rotate_ccw)
root.bind("a", block_left)
root.bind("d", block_right)
root.bind("s", block_down)
root.bind("w", block_harddrop)
root.bind("g", toggle_grid)
root.bind("f", hold)

root.bind("r", reset)

root.bind("p", toggle_pause)
root.after(delay, loop)
root.mainloop()
