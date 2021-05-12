#!/usr/bin/python3
import colorsys
import random
import copy


class Generator:
	def __init__(self, num_lights, num_colors):
		self.num_lights = num_lights
		self.num_colors = num_colors

	def next_color_rainbow(self, color):
		r = color[0] / 255
		g = color[1] / 255
		b = color[2] / 255
		h, s, v = colorsys.rgb_to_hsv(r, g, b)
		h += 0.9/self.num_colors
		r,g,b = colorsys.hsv_to_rgb(h, 1, 1)
		return (int(r * 255), int(g * 255), int(b * 255))

	def generate_rainbow_frames(self, num_frames):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

		for i in range(num_frames):
			color = self.next_color_rainbow(color)
			frame = []
			for light in range(self.num_lights):
				frame.append(color)
			frames.append(frame)
		return frames

	def generate_flow_frames(self, num_frames):
		frames = []
		colors = []
		start = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
		colors.append(start)

		for i in range(1, self.num_lights):
			colors.append(self.next_color_rainbow(colors[i - 1]))


		for frame in range(num_frames):
			color = self.next_color_rainbow(colors[-1])
			colors = colors[1:]
			colors.append(color)
			frames.append(copy.deepcopy(colors))
		return frames

	def generate_dot_frames(self, num_frames):
		frames = []
		buff = []
		white = (255, 255, 255)
		off = (0, 0, 0)

		for i in range(self.num_lights):
			colors = []
			for j in range(self.num_lights):
				if j == i:
					colors.append(white)
				else:
					colors.append(off)
			buff.append(colors)


		forward = True
		for i in range(int(num_frames/self.num_lights)):
			if forward:
				for colors in buff:
					frames.append(colors)
				forward = False
			else:
				for colors in reversed(buff):
					frames.append(colors)
				forward = True
		return frames

	def generate_radiate_frames(self, num_frames):
		frames = []
		colors = []
		start = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
		colors.append(start)

		for i in range(1, int(self.num_lights / 2)):
			colors.append(self.next_color_rainbow(colors[i - 1]))

		for frame in range(num_frames):
			color = self.next_color_rainbow(colors[-1])
			colors = colors[1:]
			colors.append(color)
			frame = copy.deepcopy(colors)
			reversed_frames = copy.deepcopy(colors)
			reversed_frames.reverse()
			frame.extend(reversed_frames)
			frames.append(frame)
		return frames








