import board
import neopixel
import time
import colorsys
import random


num_lights = 50
num_colors = 25

pixels = neopixel.NeoPixel(board.D18, num_lights)


def SetColors(buff, pixels):
	for i in range(len(pixels)):
		pixels[i] = buff[i]
	pixels.show()


def NextColor(color):
	r = color[0] / 255
	g = color[1] / 255
	b = color[2] / 255
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	h += 0.9/num_colors
	r,g,b = colorsys.hsv_to_rgb(h, 1, 1)
	return (r * 255, g * 255, b * 255)


colors = []
start = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
colors.append(start)

for i in range(1, num_lights):
	colors.append(NextColor(colors[i - 1]))


for i in range(10000):
	color = NextColor(colors[-1])
	colors = colors[:-1]
	colors.insert(0, color)
	SetColors(colors, pixels)
	# time.sleep(0.05)

