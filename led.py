#!/usr/bin/python3
import board
import neopixel
import atexit
import queue
import threading
from encoder import Encoder

# Byte structure: based on the num_lights we need to create a list of lists frames = [[RGB values for num_ligts]]
# RGB values will be encoded via chunks of 3 bytes
# So the size of the individual arrays will be of length 3 * num_lights


class Led:
	def __init__(self, num_lights, num_colors):
		self.pixels = neopixel.NeoPixel(board.D18, num_lights, auto_write=false)
		self.encoder = Encoder(num_lights, num_colors)
		atexit.register(self.on_exit)
		self.num_lights = num_lights
		self.num_colors = num_colors
		self.queue = queue.Queue()


	def put(self, compressed):
		self.queue.put(compressed)


	def pop_decode_write(self):
		while True:
			self.write(self.encoder.decode(self.queue.get()))
		

	def run(self):
		threading.Thread(target=self.pop_decode_write).start()

	def write(self, frames):
		for buff in frames:
			for i in range(self.num_lights):
				self.pixels[i] = buff[i]
			self.pixels.show()
		return

	def on_exit(self):
		self.pixels.deinit()
		print("I'm ending! Goodbye :D")


# tester = Led(50, 250)

# test_frames = tester.encoder.generate_rainbow_frames(100)

# eframes = tester.encoder.encode(test_frames)
# print(eframes)
# dframes = tester.encoder.decode(eframes)
# print(len(dframes))
# print(len(dframes[0]))

# tester.run()

# for i in range(0, 10):
# 	tester.put(eframes)




