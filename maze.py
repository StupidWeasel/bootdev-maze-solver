import time
import random
from gui_objects import Point, Cell, Square

class Maze:
	def __init__(self, window=None, seed=None, top=25, left=25, num_rows=20, num_cols=20, cell_size=25):
		self._window = window
		self._canvas = window.get_canvas() if self._window else None
		self._pos = (top, left, top+(num_rows*cell_size), left+(num_cols*cell_size))
		self._num_rows = num_rows
		self._num_cols = num_cols
		self._cell_size = cell_size
		self._cells = []
		self._seed = seed
		self._create_cells()

	def _create_cells(self):

		top, left = self._pos[0], self._pos[1]
		for row in range(self._num_rows):
			self._cells.append([])
			for col in range(self._num_cols):
				self._cells[row].append(Cell(window=self._window, top=top, left=left, size=self._cell_size))
				left += self._cell_size
			left = self._pos[1]
			top += self._cell_size

		self._post_create()

	def _animate(self,dur=0.01):
		if self._window:
			self._window.redraw()
			time.sleep(dur)

	def _post_create(self):
		if self._window:
			for i, row in enumerate(self._cells):
				for cell in row:
					cell.draw()
					self._animate(0.005)

		self._break_entrance_and_exit()
		if self._seed is not None:
			random.seed(self._seed)
		self._break_walls_r()
		self._reset_cells_visited()
		self._solve_r()

	def _break_entrance_and_exit(self):
		entrance_cell = self._cells[0][0]
		exit_cell = self._cells[-1][-1]

		entrance_cell.remove_wall("left")
		entrance_cell.set_special("start")
		exit_cell.remove_wall("right")
		exit_cell.set_special("end")

		if self._window:
			entrance_cell_pos = entrance_cell.get_pos()
			entrance_square = Square(	window=self._window,
										pos=(	Point(entrance_cell_pos[0], entrance_cell_pos[1]),
												Point(entrance_cell_pos[2], entrance_cell_pos[3])),
										fill="#CBC3E3"
										)
			exit_cell_pos = exit_cell.get_pos()
			exit_square = Square(	window=self._window,
										pos=(	Point(exit_cell_pos[0], exit_cell_pos[1]),
												Point(exit_cell_pos[2], exit_cell_pos[3])),
										fill="#00FFFF"
										)

			entrance_square.draw()
			exit_square.draw()

	def _break_walls_r(self,row=0,col=0):
		while True:
			self._animate()
			current = self._cells[row][col]
			current.visit()
			choices = []
			if col>0 and not self._cells[row][col-1].visited(): #left
				choices.append((row,col-1,"left","right"))
			if col+1<self._num_cols and not self._cells[row][col+1].visited(): #right
				choices.append((row,col+1,"right","left"))
			if row>0 and not self._cells[row-1][col].visited(): #up
				choices.append((row-1,col,"top","bottom"))
			if row+1<self._num_rows and not self._cells[row+1][col].visited(): #down
				choices.append((row+1,col,"bottom","top"))

			if not choices:
				return

			choice = random.choice(choices)
			target = self._cells[choice[0]][choice[1]]
			current.remove_wall(choice[2])
			target.remove_wall(choice[3])

			self._break_walls_r(choice[0],choice[1])


	def _solve_r(self, row=0, col=0):

		self._animate()
		current = self._cells[row][col]
		current.visit()
		choices = []

		can_move = lambda c,d: not c.visited() and not c.has_wall(d)
		if col>0 and can_move(self._cells[row][col-1],"right"): # move left
			choices.append((row,col-1))
		if col+1<self._num_cols and can_move(self._cells[row][col+1], "left"): #right
			choices.append((row,col+1))
		if row>0 and can_move(self._cells[row-1][col], "bottom"): #up
			choices.append((row-1,col))
		if row+1<self._num_rows and  can_move(self._cells[row+1][col], "top"): #down
			choices.append((row+1,col))

		if not choices:
			return False

		for choice in choices:
			cell = self._cells[choice[0]][choice[1]]
			if cell.get_special("end"):
				move_line = current.draw_move(cell, winner=True)
				return True

		choice = random.choice(choices)
		target = self._cells[choice[0]][choice[1]]

		move_line = current.draw_move(target)
		move = self._solve_r(row=choice[0], col=choice[1])
		if move: 
			if self._canvas:
				move_line.delete(self._canvas)
			move_line = current.draw_move(target, winner=True)
			self._animate()
			return True
		if self._canvas:
			move_line.delete(self._canvas)
		move_line = current.draw_move(target, undo=True)
		return self._solve_r(row=row, col=col)


	def _reset_cells_visited(self):

		for row in self._cells:
			for cell in row:
				cell.unvisit()


