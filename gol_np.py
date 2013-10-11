#!/usr/bin/env pypy
import numpypy
from random import randint as r
import numpy as np



class Universe(object):
	def __init__(self, x, y):
		prod = x * y
		self.a = np.array(np.ones_like(np.arange(prod).reshape((x,y))), dtype=bool)
		self.xlen = x
		self.ylen = y
		self.cardinals = self.north, self.north_east, self.north_west, self.west,\
			               self.east, self.south, self.south_east, self.south_west
		self.live_points = set()
		self.dead_points = set()

	def val(self, point):
		x, y = point
		return self.a[x][y]

	def on_plane(self, point):
		x, y = point
		all_positive = y >= 0 and x >= 0
		doesnt_exceed_length = x <= (self.xlen - 1) and y <= (self.ylen - 1)
		return point if all_positive and doesnt_exceed_length else False

	def north(self, point):
		return point[0], point[1] - 1

	def west(self, point):
		return point[0] - 1, point[1]

	def east(self, point):
		return point[0] + 1, point[1]

	def south(self, point):
		return point[0], point[1] + 1

	def north_west(self, point):
		return self.north(self.west(point))

	def north_east(self, point):
		return self.north(self.east(point))

	def south_east(self, point):
		return self.south(self.east(point))

	def south_west(self, point):
		return self.south(self.west(point))

	def neighbors(self, point):
		neighbor_coords = set()
		for cardinal in self.cardinals:
			potential_neighbor = cardinal(point)
			if self.on_plane(potential_neighbor):
				neighbor_coords.add(potential_neighbor)

		return neighbor_coords

	def live(self, point):
		x, y = point
		self.a[x][y] = True

	def die(self, point):
		x, y = point
		self.a[x][y] = False

	def fill_random(self, percent=.50):
		lx, ly = self.xlen, self.ylen
		how_many = int(lx  * ly * percent)
		for x in range(how_many):
			rnd_pnt = (r(0, lx - 1), r(0, ly - 1))
			self.live(rnd_pnt)

	def _indices(self):
		return {(x, y) for x in xrange(self.xlen) for y in xrange(self.ylen)}

	def _live_points(self):
		return {(x, y) for x in xrange(self.xlen) for y in xrange(self.ylen) if self.a[x][y]}

	def _dead_points(self):
		return {(x, y) for x in xrange(self.xlen) for y in xrange(self.ylen) if not self.a[x][y]}


	def _two_few_neighbors(self, num):
		return True if num < 2 else False

	def _two_three_neighbors(self, num):
		return True if 2 <= num <= 3 else False

	def _three_neighbors(self, num):
		return True if num > 3 else False

	def _dead_with_three_live(self, num):
		return True if num == 3 else False

	def _step(self):
		self.live_points = self._live_points()
		self.dead_points = self._dead_points()

		to_live, to_die = set(), set()

		for point in self.live_points:
			neighbors = self.neighbors(point)
			live_neighbors = len({neighbor for neighbor in neighbors if self.val(neighbor)})

			if self._two_few_neighbors(live_neighbors):
				to_die.add(point)
			elif self._two_three_neighbors(live_neighbors):
				to_live.add(point)
			elif self._three_neighbors(live_neighbors):
				to_die.add(point)

		for dead in self.dead_points:
			neighbors = self.neighbors(dead)
			live_neighbors = len({neighbor for neighbor in neighbors if self.val(neighbor)})

			if self._dead_with_three_live(live_neighbors):
				to_live.add(dead)

		return to_live, to_die

	def tick(self):
		to_live, to_die = self._step()
		for point in to_live:
			self.live(point)

		for point in to_die:
			self.die(point)


def main():
	u = Universe(100, 100)
	u.fill_random(.4)
	test = xrange(1000)
	for x in test:
		u.tick()



if __name__ == "__main__":
	main()