import board
import neopixel
import time
import colorsys
import random
import atexit


num_lights = 50
num_colors = 100

pixels = neopixel.NeoPixel(board.D18, num_lights)

def on_exit():
	pixels.deinit()
atexit.register(on_exit)

def SetColors(buff, pixels):
	for i in range(len(pixels)):
		pixels[i] = buff[i]
	pixels.show()


buff = []
white = (255, 255, 255)
off = (0, 0, 0)

for i in range(num_lights):
	colors = []
	for j in range(num_lights):
		if j == i:
			colors.append(white)
		else:
			colors.append(off)
	buff.append(colors)


forward = True
for i in range(10000):
	if forward:
		for colors in buff:
			SetColors(colors, pixels)
		forward = False
	else:
		for colors in reversed(buff):
			SetColors(colors, pixels)
		forward = True
	
