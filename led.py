# import board
# import neopixel
import time
import colorsys
import random
import atexit
import zlib


# Byte structure: based on the num_lights we need to create a list of lists frames = [[RGB values for num_ligts]]
# RGB values will be encoded via chunks of 3 bytes
# So the size of the individual arrays will be of length 3 * num_lights


class Led:
	def __init__(self, num_lights, num_colors):
		self.pixels = neopixel.NeoPixel(board.D18, num_lights)
		atexit.register(self.on_exit)
		self.num_lights = num_lights
		self.num_colors = num_colors

	def Write(self, buff):
		for i in range(self.num_lights):
			self.pixels[i] = buff[i]
		self.pixels.show()
		return


	def FrameToByteArr(self, frame):
		if max(frame) > 255:
			return None
		return bytearray(frame)

	def ByteArrToFrame(self, byte_arr):
		frame = []
		for byte in range(0, len(byte_arr), 3):
			r = byte_arr[byte]
			g = byte_arr[byte+1]
			b = byte_arr[byte+2]

			color = (r, g, b)
			frame.append(color)
		return frame



	def Flatten(self, frame):
		return [i for sub in frame for i in sub]

	def FlattenFrames(self, frames):
		return [i for sub in self.FlattenFrame(frame) for i in sub]


	def Encode(self, frames):
		byte_arrs = []
		frames = self.Flatten(self.Flatten(frames))
		byte_arr = self.FrameToByteArr(frames)

		return zlib.compress(byte_arr)


	def Decode(self, compressed):
		frames = []
		byte_arr = zlib.decompress(compressed)

		num_bytes_in_frame = self.num_lights*3

		for i in range(0, len(byte_arr), num_bytes_in_frame):
			frames.append(self.ByteArrToFrame(byte_arr[i:i+num_bytes_in_frame]))

		return frames


	def NextColor_Rainbow(self, color):
		r = color[0] / 255
		g = color[1] / 255
		b = color[2] / 255
		h, s, v = colorsys.rgb_to_hsv(r, g, b)
		h += 0.9/self.num_colors
		r,g,b = colorsys.hsv_to_rgb(h, 1, 1)
		return (int(r * 255), int(g * 255), int(b * 255))

	def on_exit(self):
		self.pixels.deinit()
		print("I'm ending! Goodbye :D")


tester = Led(50, 500)

test_frames = []

color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

for num_frames in range(100):
	color = tester.NextColor_Rainbow(color)
	frame = []
	for light in range(tester.num_lights):
		frame.append(color)
	test_frames.append(frame)

eframes = tester.Encode(test_frames)
print(eframes)
dframes = tester.Decode(eframes)
print(dframes)
print(len(dframes))
print(len(dframes[0]))

tester.Write(dframes)



