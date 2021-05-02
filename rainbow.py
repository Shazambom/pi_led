import board
import neopixel
import time
import numpy as np


num_lights = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

#I need all combinations of R,G,B and I need to iterate over all of them
#I need colors from ROYGBIV but I want it to transition in between these colors seamlessly so 
#I want a function I can imput the current value and it know how to step to the next color


def NextColor(color):
	out = np.sin(np.array(color) * np.pi / 180.)
	return (out[0], out[1], out[2])


color = (255, 0, 100)
while True:
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)

