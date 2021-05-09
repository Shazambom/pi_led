#!/usr/bin/python3
import zlib

# Byte structure: based on the num_lights we need to create a list of lists frames = [[RGB values for num_ligts]]
# RGB values will be encoded via chunks of 3 bytes
# So the size of the individual arrays will be of length 3 * num_lights


class Encoder:
	def __init__(self, num_lights, num_colors):
		self.num_lights = num_lights
		self.num_colors = num_colors

	def int_arr_to_byte_arr(self, frame):
		if max(frame) > 255:
			return None
		return bytearray(frame)

	def byte_arr_to_frame(self, byte_arr):
		frame = []
		for byte in range(0, len(byte_arr), 3):
			r = byte_arr[byte]
			g = byte_arr[byte+1]
			b = byte_arr[byte+2]

			color = (r, g, b)
			frame.append(color)
		return frame


	def flatten(self, arr):
		return [i for sub in arr for i in sub]


	def encode(self, frames):
		byte_arrs = []
		frames = self.flatten(self.flatten(frames))
		byte_arr = self.int_arr_to_byte_arr(frames)

		return zlib.compress(byte_arr)


	def decode(self, compressed):
		frames = []
		byte_arr = zlib.decompress(compressed)

		num_bytes_in_frame = self.num_lights*3

		for i in range(0, len(byte_arr), num_bytes_in_frame):
			frames.append(self.byte_arr_to_frame(byte_arr[i:i+num_bytes_in_frame]))

		return frames




