from gol import Universe as U
import pyglet
from random import random as r


def pyglet_way():
	x, y = 120, 120

	u = U(x, y)

	scale = 1
	x *= scale
	y *= scale

	red, blue, green, alpha = \
		(
		lambda tup, magnitude: (tup[0] + magnitude, tup[1], tup[2], tup[3]),
		lambda tup, magnitude: (tup[0], tup[1], tup[2] + magnitude, tup[3]),
		lambda tup, magnitude: (tup[0], tup[1] + magnitude, tup[2], tup[3]),
		lambda tup, magnitude: (tup[0], tup[1], tup[2], tup[3] + magnitude)
		)


	black = 0.0, 0.0, 0.0, 1.0
	white = red(green(blue(black, 1.0), 1.0), 1.0)
	purple = red(blue(alpha(black, 0.5), 0.5), 0.5)
	color = white
	set_live_color = pyglet.gl.glColor4f

	window = pyglet.window.Window(width=x, height=y)
	set_live_color(*color)

	gl_draw_sq = pyglet.graphics.draw_indexed
	four, gl_flag, indices = 4, 'v2i', (0, 1, 2, 0, 2, 3)

	def draw_square(point, size=1):
		x, y = point[0] * size, point[1] * size
		x_size, y_size = x + size, y + size
		vertices = x,y, x_size,y, x_size,y_size, x,y_size
		gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))


	def process_living(living):
		for live in living:
			if u.val(live):
				draw_square(live, scale)

	def on_draw(self):
		window.clear()
		derp()


	@window.event
	def on_mouse_press(*args):
		u.fill_random(.4)

	def derp():
		u.tick()
		process_living(u.live_points)

	fps_display = pyglet.clock.ClockDisplay()
	fps_display.draw()
	pyglet.clock.schedule(on_draw)
	pyglet.app.run()

if __name__ == "__main__":
	pyglet_way()

