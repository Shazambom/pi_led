#!/usr/bin/python3
import colorsys
import random
import copy
from sorting import Sorter



off = (0, 0, 0)
white = (255, 255, 255)

class Generator:
	def __init__(self, num_lights, num_colors, height):
		self.num_lights = num_lights
		self.num_colors = num_colors
		self.height = height
		self.width = int(num_lights / height)
		self.generate_table()


	def generate_table(self):
		self.lookup = []
		count = 0
		for w in range(self.width):
			column = []
			for h in range(self.height):
				column.append(count)
				count += 1 
			# We're doing this weird reverse thing because even though it'll look wrong on a grid of pixels this will look correct when using the 
			# actual LEDs because have to have the numbered lights near one another
			if w % 2 == 1:
				column.reverse()
			self.lookup.append(column)


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

	def generate_cascade_frames(self):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

		board = [off] * self.num_lights

		for light in range(0, self.num_lights):
			color = self.next_color_rainbow(color)
			x = self.width - 1 
			y = light % self.height
			pos = self.lookup[x][y]
			
			board[pos] = color
			frames.append(copy.deepcopy(board))
			
			for sl in range(self.width):
				x -= 1
				if pos - self.height < 0 or board[self.lookup[x][y]] != off:
					break
				board[pos] = off
				pos = self.lookup[x][y]
				board[pos] = color
				frames.append(copy.deepcopy(board))
		return frames

	def generate_snake_frames(self):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

		board = [off] * self.num_lights

		for light in range(0, self.num_lights):
			color = self.next_color_rainbow(color)
			y = light % self.height
			pos = self.lookup[self.width - 1][y]
			
			board[pos] = color
			frames.append(copy.deepcopy(board))
			
			for x in range(self.width -1, -1, -1):
				if pos - self.height < 0 or board[self.lookup[x][y]] != off:
					itter = board[1:pos]
					color = self.next_color_rainbow(color)
					itter.append(color)
					board[0:pos] = itter
					break
				board[pos] = off
				pos = self.lookup[x][y]
				board[pos] = color
				frames.append(copy.deepcopy(board))
		return frames

	def generate_game_of_life_frames(self, num_frames):
		boards = []
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))

		b_width = self.width * 3
		b_height = self.height * 5

		board = []
		for x in range(b_width):
			row = []
			for y in range(b_height):
				if bool(random.getrandbits(1)):
					row.append(1)
				else:
					row.append(0)
			board.append(row)

		neighbors = []
		for x in range(b_width):
			row = []
			for y in range(b_height):
				row.append(self.get_neighbors(x, y, b_width, b_height))
			neighbors.append(row)


		buff = copy.deepcopy(board)

		for frame in range(num_frames):
			for x in range(b_width):
				for y in range(b_height):
					alive = 0
					for neighbor in neighbors[x][y]:
						alive += board[neighbor[0]][neighbor[1]]
					if (board[x][y] == 1 and alive == 2) or alive == 3:
						buff[x][y] = 1
					else:
						buff[x][y] = 0
			board = copy.deepcopy(buff)
			boards.append(board)


		height_offset = int((b_height - self.height)/ 2)
		width_offset = int((b_width - self.width)/ 2)
		for board in boards:
			frame = [off] * self.num_lights
			for x in range(self.width):
				adj_x = x + width_offset
				for y in range(self.height):
					adj_y = y + height_offset
					if board[adj_x][adj_y] == 1:
						frame[self.lookup[x][y]] = color
					else:
						frame[self.lookup[x][y]] = off
			color = self.next_color_rainbow(color)
						
			
			frames.append(frame)


		return frames



	def get_neighbors(self, x, y, w, h):
		return [
		self.get_safe_pos(x - 1, y - 1, w, h), 
		self.get_safe_pos(x, y - 1, w, h), 
		self.get_safe_pos(x + 1, y - 1, w, h), 
		self.get_safe_pos(x - 1, y, w, h), 
		self.get_safe_pos(x + 1, y, w, h), 
		self.get_safe_pos(x - 1, y + 1, w, h), 
		self.get_safe_pos(x, y + 1, w, h), 
		self.get_safe_pos(x + 1, y + 1, w, h)
		]

	def get_safe_pos(self, x, y, w, h):
		return ((x + w) % w, (y + h) % h)


	def generate_dance_frames(self, num_frames):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
		

		board = []
		neighbors = []
		for x in range(self.width):
			row = []
			n_row = []
			for y in range(self.height):
				if x == int(self.width / 2) and y == int(self.height / 2):
					row.append(color)
				else:
					row.append(off)
				n_row.append(self.get_neighbors(x, y, self.width, self.height))
			board.append(row)
			neighbors.append(n_row)

		buff = copy.deepcopy(board)
		for f in range(num_frames):
			frame = [off] * self.num_lights
			for x in range(self.width):
				for y in range(self.height):
					if random.randint(0, 100) < 2:
						color = self.next_color_rainbow(color)
						board[x][y] = color

					frame[self.lookup[x][y]] = board[x][y]
					if board[x][y] == off:
						avg_color = [0, 0, 0]
						for neighbor in neighbors[x][y]:
							n = board[neighbor[0]][neighbor[1]]
							avg_color[0] += n[0]
							avg_color[1] += n[1]
							avg_color[2] += n[2]
						buff[x][y] = (int(avg_color[0] / 8), int(avg_color[1] / 8), int(avg_color[2] / 8))
					else:
						decay_val = 7
						buff[x][y] = (self.decay(board[x][y][0], decay_val), self.decay(board[x][y][1], decay_val), self.decay(board[x][y][2], decay_val))

			frames.append(frame)
			board = copy.deepcopy(buff)


		return frames

	def decay(self, channel, amount):
		delta = channel - amount
		return delta if delta > 0 else 0

	def generate_sort_frames(self, func):
		frames = []
		color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
		board = []
		colors = []



		for x in range(self.width):
			colors.append(color)
			color = self.next_color_rainbow(color)

		for y in range(self.height):
			board.append(list(range(0, self.width)))

		for y in range(self.height):
			random.shuffle(board[y])

		##All the setup is done here now we just have to get frames for each swap

		frame_rows = []
		for y in range(self.height):
			frame_rows.append([copy.deepcopy(board[y])])
		

		for y in range(self.height):
			frame_rows[y].extend(self.sort_with_func(copy.deepcopy(board[y]), func))

		num_frames = max([len(row) for row in frame_rows])

		for frame_ind in range(num_frames):
			frame = [off] * self.num_lights
			for y in range(self.height):
				ind = frame_ind if frame_ind < len(frame_rows[y]) else len(frame_rows[y]) - 1
				for x in range(self.width):
					frame[self.lookup[x][y]] = colors[frame_rows[y][ind][x]]
			frames.append(frame)
		return frames

	def sort_with_func(self, lst, func):
		frame_row = []
		sorter = Sorter(lambda l: frame_row.append(l))
		if func == "merge":
			sorter.merge_sort(lst, 0, self.width-1)
		elif func == "quick":
			sorter.quick_sort(lst, 0, self.width)
		elif func == "comb":
			sorter.comb_sort(lst)
		return frame_row

	

#Fixed all the bugs, I'm gonna keep the example gif code here commented out because it may be useful for other experiments
# from PIL import Image

# gen = Generator(250, 250, 5)
# gol_frames = gen.generate_merge_frames()
# images = []
# for frame in gol_frames:
# 	image = Image.new('RGB', (50, 5), off)
# 	for i in range(image.size[0]):
# 		for j in range(image.size[1]):
# 			image.putpixel((i, j), frame[gen.lookup[i][j]])
# 	images.append(image)

# images[0].save('gol_experiment.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)


# gen = Generator(100, 250, 5)
# e = Encoder(100, 250)

# flow_frames = gen.generate_flow_frames(1000)
# dot_frames = gen.generate_dot_frames(1000)
# radiate_frames = gen.generate_radiate_frames(1000)
# cascade_frames = gen.generate_cascade_frames(5)

# flow_f = open("flow.bin", "wb")
# dot_f = open("dot.bin", "wb")
# radiate_f = open("radiate.bin", "wb")
# cascade_f = open("cascade.bin", "wb")


# flow_f.write(e.encode(flow_frames))
# dot_f.write(e.encode(dot_frames))
# radiate_f.write(e.encode(radiate_frames))
# cascade_f.write(e.encode(cascade_frames))






