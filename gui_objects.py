
class Point:
	def __init__(self, y, x):
		self.x = x
		self.y = y

class Line:
	def __init__(self, pointa, pointb, width=2):
		self.points = (pointa, pointb)
		self.width = width
		self._id = None

	def draw(self, canvas, fill):
		if canvas:
			self._id = canvas.create_line(self.points[0].x,
								self.points[0].y,
								self.points[1].x,
								self.points[1].y,
								fill=fill,
								width=self.width)
	def delete(self, canvas):
		if canvas:
			canvas.delete(self._id)


class Square:
	def __init__(self, window=None, pos=None, fill="#FF0000"):
		self._window = window
		self._canvas = window.get_canvas() if self._window else None
		self._pos = pos
		self._fill = fill
		self._id = None


	def draw(self, lower=True, higher=False):
		if not self._pos or len(self._pos)!=2 or any(not isinstance(i, Point) for i in self._pos):
			raise Exception("Squares need two Points to be drawn")

		if not self._canvas:
			raise Exception("Can't draw a square without a canvas")

		self._id = self._canvas.create_rectangle( self._pos[0].x,
											self._pos[0].y,
											self._pos[1].x,
											self._pos[1].y,
											fill=self._fill,
											width=0)
		if lower and higher:
			return

		if lower:
			self._canvas.tag_lower(self._id)
			return
		
		if higher:
			self._canvas.tag_higher(self._id)
			return

	def delete(self):
		if self._canvas:
			self._canvas.delete(self._id)


class Cell:
	def __init__(self, window=None, top=0, left=0, size=0):
		self._window = window
		self._canvas = window.get_canvas() if self._window else None
		self._top = top
		self._left = left
		self._bottom = top+size
		self._right = left+size
		self._size = size
		self._visited = False
		self._special = set()

		self._walls = {
							#01 + 03
							"top": Line(	Point(self._top,self._left),
											Point(self._top,self._right)
										),
							#01 + 12
							"left": Line(	Point(self._top,self._left),
											Point(self._bottom,self._left)
										),
							#12 + 23 
							"bottom": Line(	Point(self._bottom,self._left),
											Point(self._bottom,self._right)
										),
							#03 + 23
							"right": Line(	Point(self._top,self._right),
											Point(self._bottom,self._right)
										)}
	
	def get_pos(self):
		return (self._top, self._left, self._bottom, self._right)

	def get_center(self):
		half = self._size//2
		return (self._top+half, self._left+half)

	def draw_move(self, target_cell, undo=False, winner=False):
		move_line = Line(Point(*self.get_center()),Point(*target_cell.get_center()))
		
		colour = "#00FFFF" if winner else "#808080" if undo else "#FF0000"
		move_line.draw(self._canvas,colour)
		return move_line

	def draw(self, fill="#000000"):
		for side, line in self._walls.items():
			
			#colour_test={"top":"blue", "left":"green", "bottom":"orange", "right":"purple"}
			if line:
				line.draw(self._canvas, fill)

	def visited(self):
		return self._visited

	def visit(self):
		self._visited = True

	def unvisit(self):
		self._visited = False

	def set_special(self, special):
		self._special.add(special)

	def get_special(self, special):
		return special in self._special

	def remove_special(self, special):
		if special in self._special:
			self._special.remove(special)

	def has_wall(self, wall):
		if not wall in self._walls:
			raise Exception("Can't check wall, invalid wall type")

		return True if self._walls[wall] else False

	def remove_wall(self, wall):
		if not wall in self._walls:
			raise Exception("Can't remove wall, invalid wall type")
		if not self._walls[wall]:
			return
		if self._canvas:
			self._walls[wall].delete(self._canvas)
		self._walls[wall] = False

