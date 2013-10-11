from gol import Universe as U
from random import randint as r
import pygame
from pygame.gfxdraw import rectangle as rect
from pygame import MOUSEBUTTONUP as M
import pyglet


def conway_frames():
	while True:
		u.tick()
		yield u.live_points, u.dead_points


def pygame_way():
	x, y = 100, 100
	rect_size = 1
	scale = 5
	u = U(x, y)
	u.fill_random(.4)
	white, black = (255, 255, 255), (0, 0, 0)


	def process_living(living):
		for live in living:
			if u.val(live):
				x1, y1 = live
				rect(screen, (x1 * scale, y1 * scale, rect_size, rect_size), white)
			#p(screen, x1, y1, white)

	def process_dead(dead):
		for died in dead:
			if not u.val(died):
				x1, y1 = died
				rect(screen, (x1 * scale, y1 * scale, rect_size, rect_size), black)
			#p(screen, x1, y1, black)

	def get_click():
		ev = pygame.event.get()
		for event in ev:
			if event.type == M:
				u.fill_random(.4)


	pygame.init()
	x *= scale
	y *= scale
	rect_size *= scale
	screen = pygame.display.set_mode((x, y))

	for living, dead in conway_frames():
		process_dead(dead)


	process_living(living)
	get_click()
	pygame.display.flip()


def pyglet_way():
	x, y = 100, 100
	point = x, y
	rect_size = 1
	scale = 5
	u = U(*point)
	u.fill_random(.4)
	white, black = (255, 255, 255), (0, 0, 0)
	x *= scale
	y *= scale
	rect_size *= scale
	window = pyglet.window.Window(width=x, height=y)

	def draw_square(point, size):
		x, y = point
		xs, ys = x+size, y+size
		vertices = (x,y, xs,y, xs,ys, x,ys)
		indices = [0, 1, 2, 0, 2, 3]
		pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, indices, ('v2i', vertices))



	@window.event
	def on_draw():
		window.clear()
		pyglet.gl.glColor4f(1.0, 0, 0, 1.0)
		point, size = (1,1), scale
		draw_square(point, size)
		point = (100, 100)

	pyglet.app.run()

if __name__ == "__main__":
	pyglet_way()

