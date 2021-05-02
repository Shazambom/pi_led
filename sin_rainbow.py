import board
import neopixel
import time
import numpy as np
import random

num_lights = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

#I need all combinations of R,G,B and I need to iterate over all of them
#I need colors from ROYGBIV but I want it to transition in between these colors seamlessly so 
#I want a function I can imput the current value and it know how to step to the next color


def NextColor(color):
	cin = np.true_divide(np.array(color), 255) * 360
	rad = np.absolute(np.sin(cin * np.pi / 180.))
	
	return (rad[0] * 255, rad[1] * 255, rad[2] * 255)


color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
for i in range(10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)
	time.sleep(0.5)

