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
	cin = np.true_divide(np.array(color), 255) * 360
	print("Angle IN: " + str(cin))
	rad = np.absolute(np.sin(cin * np.pi / 180.))
	print("Radians out: " + str(rad))
	ang = rad / np.pi
	print("% Of angle: " + str(ang))
	
	return (ang[0] * 255, ang[1] * 255, ang[2] * 255)


color = (255, 127, 63)
for i in range(0, 10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)
	print(color)
	time.sleep(0.1)

