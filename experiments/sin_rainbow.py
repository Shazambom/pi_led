import board
import neopixel
import time
import numpy as np
import random
import atexit


num_lights = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

def on_exit():
	pixels.deinit()
atexit.register(on_exit)


def NextColor(color):
	cin = np.true_divide(np.array(color), 255) * 360
	rad = np.absolute(np.sin(cin * np.pi / 360.))
	
	return (rad[0] * 255, rad[1] * 255, rad[2] * 255)


color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
for i in range(10000):
	pixels.fill(color)
	pixels.show()
	color = NextColor(color)
	time.sleep(0.5)

