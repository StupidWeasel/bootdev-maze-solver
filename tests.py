import unittest
from maze import Maze

class Tests(unittest.TestCase):

	def test_maze_create_cells(self):

		m1 = Maze(num_cols=12, num_rows=12, cell_size=10)
		self.assertEqual(
			len(m1._cells),
			12,
		)
		self.assertEqual(
			len(m1._cells[0]),
			12,
		)

	def test_maze_visit_and_unvisit_cells(self):

		maze = Maze(num_cols=1, num_rows=1, cell_size=10)
		print(maze._cells[0][0].visited())
		self.assertTrue(maze._cells[0][0].visited()) # First cell is visited, then reset, then visited again

		maze._cells[0][0].unvisit() # Force unvisit
		self.assertFalse(maze._cells[0][0].visited())
		
		maze._cells[0][0].visit() # Visit again
		self.assertTrue(maze._cells[0][0].visited()) # Now visited

		maze._cells[0][0].unvisit() # Force unvisit
		self.assertFalse(maze._cells[0][0].visited())

		maze._cells[0][0].visit() # Visit again
		self.assertTrue(maze._cells[0][0].visited()) # Now visited
		
		maze._reset_cells_visited() # Unvisit all
		self.assertFalse(maze._cells[0][0].visited()) # Now unvisited?

if __name__ == "__main__":
	unittest.main()
