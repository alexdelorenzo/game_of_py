__author__ = 'alex'

import unittest


class MyTestCase(unittest.TestCase):
	def setUp(self):
		import game_of_pyfe
		self.U = game_of_pyfe.Universe
		self.u = self.U(*(10, 10))

	def tearDown(self):
		pass

	def test_can_import_universe(self):
		from game_of_pyfe import Universe
		self.assertTrue(Universe)

	def test_can_init(self):
		import game_of_pyfe
		test = (1, 1)
		u = game_of_pyfe.Universe(*test)
		self.assertTrue(isinstance(u, game_of_pyfe.Universe))

	def test_len_reflects_choords(self):
		test_choords = (10, 10)
		lengths = len(self.u), len(self.u[0])
		self.assertEqual(test_choords, lengths)

	def test_return_origin_neighbors(self):
		origin = (0, 0)
		east, south, south_east = (1, 0), (0, 1), (1, 1)
		confirmed = east, south, south_east
		neighbors = self.u.neighbors(origin)
		self.assertEqual(len(confirmed), len(neighbors))
		for neighbor in neighbors:
			self.assertTrue(neighbor in confirmed)

	def test_doesnt_return_nonexistent(self):
		origin = (0, 0)
		west, north, north_west = (-1, 0), (0, -1), (-1, -1)
		dont_exist = west, north, north_west
		neighbors = self.u.neighbors(origin)
		for neighbor in neighbors:
			self.assertTrue(neighbor not in dont_exist)

	def test_can_add_cell(self):
		live_cell = (1, 1)
		self.u.live(live_cell)
		self.assertTrue(self.u[1][1])

	def test_can_kill_cell(self):
		dead_cell = (1, 1)
		self.u.die(dead_cell)
		self.assertFalse(self.u[1][1])

	def test_step_kills_cells_with_less_than_2_neighbors(self):
		live_points = [(0, 0), (0, 1)]

		for point in live_points:
			self.u.live(point)

		neighbors = self.u.neighbors((0, 0))
		live_neighbors = [neighbor for neighbor in neighbors if self.u.val(neighbor)]
		self.assertEqual(1, len(live_neighbors))
		to_live, to_die = self.u._step

		self.assertEqual(live_points, to_die)
		for point in live_points:
			self.assertTrue(point not in to_live)

	def test_step_two_three_neighbors_live(self):
		live_points = [(0, 0), (0, 1), (0, 2), (1, 1)]
		should_live = live_points[1:]

		for point in live_points:
			self.u.live(point)

		neighbors = self.u.neighbors((0, 1))
		live_neighbors = [neighbor for neighbor in neighbors if self.u.val(neighbor)]
		self.assertEqual(3, len(live_neighbors))

		to_live, to_die = self.u._step

		for should in should_live:
			self.assertTrue(should in to_live)

	def test_step_more_than_three_die(self):
		live_points = [(0, 0), (0, 1), (2, 0), (1, 0), (1, 1)]
		should_live = live_points[1:]

		for point in live_points:
			self.u.live(point)

		neighbors = self.u.neighbors((1, 0))
		live_neighbors = [neighbor for neighbor in neighbors if self.u.val(neighbor)]
		self.assertEqual(4, len(live_neighbors))

		to_live, to_die = self.u._step

		should_die = [(1, 0), (1, 1)]
		should_live = [(0, 0), (0, 1), (2, 0)]

		for should in should_live:
			self.assertTrue(should in to_live)

		for should in should_die:
			self.assertTrue(should in to_die)

	def test_step_dead_with_three_live(self):
		live_points = [(0, 0), (0, 1), (2, 0), (1, 0), (1, 1)]

		for point in live_points:
			self.u.live(point)

		neighbors = self.u.neighbors((1, 0))
		live_neighbors = [neighbor for neighbor in neighbors if self.u.val(neighbor)]
		self.assertEqual(4, len(live_neighbors))

		to_live, to_die = self.u._step

		self.assertTrue((2, 1) in to_live)

	def test_does_tick_apply_changes_from_step(self):
		live_points = [(0, 0), (0, 1), (2, 0), (1, 0), (1, 1)]

		for point in live_points:
			self.u.live(point)

		neighbors = self.u.neighbors((1, 0))
		live_neighbors = [neighbor for neighbor in neighbors if self.u.val(neighbor)]
		self.assertEqual(4, len(live_neighbors))

		to_live, to_die = self.u._step

		should_die = [(1, 0), (1, 1)]
		should_live = [(0, 0), (0, 1), (2, 0), (2, 1)]

		self.u.tick()

		for should in should_live:
			self.assertTrue(self.u.val(should) == True)

		for should in should_die:
			self.assertTrue(self.u.val(should) == False)

if __name__ == '__main__':
	unittest.main()
