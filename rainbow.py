import board
import neopixel
import time
import colorsys
import random


num_lights = 50
num_colors = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

#I need all combinations of R,G,B and I need to iterate over all of them
#I need colors from ROYGBIV but I want it to transition in between these colors seamlessly so 
#I want a function I can imput the current value and it know how to step to the next color


def NextColor(color):
	r = color[0] / 255
	g = color[1] / 255
	b = color[2] / 255
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	h += 0.9/num_colors
	return colorsys.hsv_to_rgb(h, 1, 1)

color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
for i in range(0, 10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)
	time.sleep(0.1)

