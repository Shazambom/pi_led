import board
import neopixel
import time


num_lights = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

#I need all combinations of R,G,B and I need to iterate over all of them

colors = []

for r in range(255, -1, -1):
	for g in range(255, -1, -1):
		for b in range(255, -1, -1):
			colors.append((r, g, b))

for color in colors:
	pixels.fill(color)
	pixels.show()
	# sleep(0.1)
