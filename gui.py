from tkinter import Tk, BOTH, Canvas
from gui_objects import Point,Line, Cell

class Window:
	def __init__(self, width, height, title):
		self._root = Tk()
		self._root.title(title)
		self._active = False
		self._canvas = Canvas(self._root, height=height, width=width, bg="#ffffff")
		self._canvas.pack(fill="both", expand=1)
		
		self._root.protocol("WM_DELETE_WINDOW", self.close)
		self.center_window()

	def center_window(self):
		self._root.update_idletasks()
		width = self._root.winfo_width()
		height = self._root.winfo_height()
		screen_width = self._root.winfo_screenwidth()
		screen_height = self._root.winfo_screenheight()
		x = (screen_width - width) // 2
		y = (screen_height - height) // 2
		self._root.geometry(f"{width}x{height}+{x}+{y}")

	def redraw(self):
		self._root.update_idletasks()
		self._root.update()

	def wait_for_close(self):
		self._active = True
		while self._active:
			self.redraw()
		print("Closed window")

	def close(self):
		self._active = False

	def draw_line(self, line, fill):
		line.draw(self._canvas, fill)

	def create_cell(self, top=None, left=None, size=25):
		if not top or not left:
			raise Exception("Both top & left arguments needed")
		return Cell(top, left, size, self._canvas)

	def get_canvas(self):
		return self._canvas

