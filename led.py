import board
import neopixel
import time
import colorsys
import random
import atexit
import zlib
import copy
import queue
import threading
from encoder import Encoder

# Byte structure: based on the num_lights we need to create a list of lists frames = [[RGB values for num_ligts]]
# RGB values will be encoded via chunks of 3 bytes
# So the size of the individual arrays will be of length 3 * num_lights


class Led:
	def __init__(self, num_lights, num_colors):
		self.pixels = neopixel.NeoPixel(board.D18, num_lights)
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

	# def int_arr_to_byte_arr(self, frame):
	# 	if max(frame) > 255:
	# 		return None
	# 	return bytearray(frame)

	# def byte_arr_to_frame(self, byte_arr):
	# 	frame = []
	# 	for byte in range(0, len(byte_arr), 3):
	# 		r = byte_arr[byte]
	# 		g = byte_arr[byte+1]
	# 		b = byte_arr[byte+2]

	# 		color = (r, g, b)
	# 		frame.append(color)
	# 	return frame


	# def flatten(self, arr):
	# 	return [i for sub in arr for i in sub]


	# def encode(self, frames):
	# 	byte_arrs = []
	# 	frames = self.flatten(self.flatten(frames))
	# 	byte_arr = self.int_arr_to_byte_arr(frames)

	# 	return zlib.compress(byte_arr)


	# def decode(self, compressed):
	# 	frames = []
	# 	byte_arr = zlib.decompress(compressed)

	# 	num_bytes_in_frame = self.num_lights*3

	# 	for i in range(0, len(byte_arr), num_bytes_in_frame):
	# 		frames.append(self.byte_arr_to_frame(byte_arr[i:i+num_bytes_in_frame]))

	# 	return frames

	# def next_color_rainbow(self, color):
	# 	r = color[0] / 255
	# 	g = color[1] / 255
	# 	b = color[2] / 255
	# 	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	# 	h += 0.9/self.num_colors
	# 	r,g,b = colorsys.hsv_to_rgb(h, 1, 1)
	# 	return (int(r * 255), int(g * 255), int(b * 255))

	# def generate_rainbow_frames(self, num_frames):
	# 	frames = []
	# 	color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

	# 	for i in range(num_frames):
	# 		color = self.next_color_rainbow(color)
	# 		frame = []
	# 		for light in range(self.num_lights):
	# 			frame.append(color)
	# 		frames.append(frame)
	# 	return frames

	# def generate_flow_frames(self, num_frames):
	# 	frames = []
	# 	colors = []
	# 	start = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
	# 	colors.append(start)

	# 	for i in range(1, self.num_lights):
	# 		colors.append(self.next_color_rainbow(colors[i - 1]))


	# 	for frame in range(num_frames):
	# 		color = self.next_color_rainbow(colors[-1])
	# 		colors = colors[1:]
	# 		colors.append(color)
	# 		frames.append(copy.deepcopy(colors))
	# 	return frames

	# def generate_dot_frames(self, num_frames):
	# 	frames = []
	# 	buff = []
	# 	white = (255, 255, 255)
	# 	off = (0, 0, 0)

	# 	for i in range(self.num_lights):
	# 		colors = []
	# 		for j in range(self.num_lights):
	# 			if j == i:
	# 				colors.append(white)
	# 			else:
	# 				colors.append(off)
	# 		buff.append(colors)


	# 	forward = True
	# 	for i in range(int(num_frames/self.num_lights)):
	# 		if forward:
	# 			for colors in buff:
	# 				frames.append(colors)
	# 			forward = False
	# 		else:
	# 			for colors in reversed(buff):
	# 				frames.append(colors)
	# 			forward = True
	# 	return frames

	def on_exit(self):
		self.pixels.deinit()
		print("I'm ending! Goodbye :D")


tester = Led(50, 250)

test_frames = tester.encoder.generate_rainbow_frames(100)

eframes = tester.encoder.encode(test_frames)
print(eframes)
dframes = tester.encoder.decode(eframes)
print(len(dframes))
print(len(dframes[0]))

tester.run()

for i in range(0, 10):
	tester.put(eframes)


# while not tester.queue.empty():
# 	tester.play()




