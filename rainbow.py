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
	cin = np.true_divide(np.array(color), 255)
	r = np.sin(cin[0] * np.pi / 180.) * 255
	g = np.sin(cin[1] * np.pi / 90.) * 255
	b = np.sin(cin[2] * np.pi / 270.) * 255
	print("R: " + str(r) + " G: " + str(g) + " B: " + str(b))
	return (r, g, b)


color = (255, 127, 63)
for i in range(0, 10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)
	sleep(0.1)

