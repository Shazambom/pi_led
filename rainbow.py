import board
import neopixel
import time
import colorsys
import random


num_lights = 50
num_colors = 500

pixels = neopixel.NeoPixel(board.D18, num_lights)



def NextColor(color):
	r = color[0] / 255
	g = color[1] / 255
	b = color[2] / 255
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	h += 0.9/num_colors
	r,g,b = colorsys.hsv_to_rgb(h, 1, 1)
	return (r * 255, g * 255, b * 255)

color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
for i in range(10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)

