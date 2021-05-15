#!/usr/bin/python3
import colorsys
import random
import copy


off = (0, 0, 0)
white = (255, 255, 255)

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

	def generate_cascade_frames(self, num_frames, height):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

		board = [off] * self.num_lights

		for light in range(0, self.num_lights):
			color = self.next_color_rainbow(color)
			rem = light % height
			pos = self.num_lights - 1 - rem
			
			board[pos] = color
			frames.append(copy.deepcopy(board))
			for sl in range(int(self.num_lights / height)):
				if pos - height < 0 or board[pos - height] != off:
					break
				board[pos] = off
				pos = pos - height
				board[pos] = color
				frames.append(copy.deepcopy(board))
		return frames











# gen = Generator(50, 250)
# e = Encoder(50, 250)

# flow_frames = gen.generate_flow_frames(1000)
# dot_frames = gen.generate_dot_frames(1000)
# radiate_frames = gen.generate_radiate_frames(1000)

# flow_f = open("flow.bin", "wb")
# dot_f = open("dot.bin", "wb")
# radiate_f = open("radiate.bin", "wb")


# flow_f.write(e.encode(flow_frames))
# dot_f.write(e.encode(dot_frames))
# radiate_f.write(e.encode(radiate_frames))






