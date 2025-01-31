import sys
from gui import Window
from maze import Maze

def main():

	seed = None
	if len(sys.argv)>1:
		seed = sys.argv[1]
		print("Starting up with seed ", sys.argv[1])
	else:
		print("Starting up")
	
	sizew = 900
	sizeh = 900
	cell_size = 30
	margin = 25

	num_cols = (sizew-(margin*2))//cell_size
	num_rows = (sizeh-(margin*2))//cell_size
	window = Window(sizew,sizeh, "Amazing Maze Solver!")

	Maze(window=window, seed=seed, top=margin, left=margin, num_cols=num_cols, num_rows=num_rows, cell_size=cell_size)
	window.wait_for_close()

if __name__ == "__main__":
	main()
