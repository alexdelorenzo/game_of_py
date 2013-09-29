class Universe(list):
	def __init__(self, x, y):
		super(Universe, self).__init__()
		for num in range(x):
			self.append([False for num in range(y)])

	def val(self, point):
		x, y = point
		return self[x][y]

	def on_plane(self, point):
		x, y = point
		all_positive = y >= 0 and x >= 0
		doesnt_exceed_length = x <= (len(self) - 1) and y <= (len(self[x]) - 1)
		return point if all_positive and doesnt_exceed_length else False

	def neighbors(self, point):

		def north(point):
			return point[0], point[1] - 1

		def west(point):
			return point[0] - 1, point[1]

		def east(point):
			return point[0] + 1, point[1]

		def south(point):
			return point[0], point[1] + 1

		def north_west(point):
			return north(west(point))

		def north_east(point):
			return north(east(point))

		def south_east(point):
			return south(east(point))

		def south_west(point):
			return south(west(point))

		cardinals = north, north_east, north_west, west, east, south, south_east, south_west
		neighbor_choords = [cardinal(point) for cardinal in cardinals if self.on_plane(cardinal(point))]
		return neighbor_choords

	def live(self, point):
		x, y = point
		self[x][y] = True

	def die(self, point):
		x, y = point
		self[x][y] = False



	@property
	def _step(self):
		def _two_few_neighbors(num):
			return True if num < 2 else False

		def _two_three_neighbors(num):
			return True if 2 <= num <= 3 else False

		def _three_neighbors(num):
			return True if num > 3 else False

		def _dead_with_three_live(num):
			return True if num == 3 else False

		live_points = [(x, y) for x in range(len(self)) for y in range(len(self[x])) if self[x][y]]
		dead_points = [(x, y) for x in range(len(self)) for y in range(len(self[x])) if not self[x][y]]

		to_live, to_die = [], []

		for point in live_points:
			neighbors = self.neighbors(point)
			live_neighbors = len([neighbor for neighbor in neighbors if self.val(neighbor)])

			if _two_few_neighbors(live_neighbors):
				to_die.append(point)
			elif _two_three_neighbors(live_neighbors):
				to_live.append(point)
			elif _three_neighbors(live_neighbors):
				to_die.append(point)

		for dead in dead_points:
			neighbors = self.neighbors(dead)
			live_neighbors = len([neighbor for neighbor in neighbors if self.val(neighbor)])

			if _dead_with_three_live(live_neighbors):
				to_live.append(dead)

		return to_live, to_die

	def tick(self):
		to_live, to_die = self._step
		for point in to_live:
			self.live(point)

		for point in to_die:
			self.die(point)

def main():
	u = Universe()


if __name__ == "__main__":
	main()