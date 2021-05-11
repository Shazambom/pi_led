import json

white = (255, 255, 255)
off = (0, 0, 0)

class Font:
	def __init__(self, height, width):
		self.height = height
		if self.height < 5:
			self.height = 5
		self.width = width
		font_file = open('font.json', 'r')
		self.font = json.load(font_file)
		font_file.close()
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


	def text_to_frames(self, text):
		#extracting the values from the characters
		font_arr = []
		for char in text.upper():
			if char in self.font:
				font_arr.append(self.font[char])
		frames = []
		slices = []
		num_slices = (self.font["width"] * len(text)) + self.width + 1


		#Adding blackspace before the scroll
		for w in range(self.width):
			slices.append([0] * self.height)

		#Computing all of the slices that each frame will have to use
		for ns in range(num_slices):
			letter = int(ns / self.font["width"])
			rem = ns % self.font["width"]
			sl = []
			for i in range(self.font["height"]):
				for j in range(self.font["width"]):
					if rem == j:
						if letter < len(font_arr):
							sl.append(font_arr[letter][i][j])
						else:
							sl.append(0)
			slices.append(sl)

		#Creating all of the frames using the slices
		for i in range(num_slices):
			frame = [off] * (self.height * self.width)
			for y in range(self.height):
				for x in range(self.width):
					if i + x < num_slices:
						sl = slices[i + x]
						if sl[y] == 1:
							frame[self.lookup[x][y]] = white
			frames.append(frame)
		return frames



# 	<----------			<----------
# 0, 9, 10, 19, 20, 29, 30, 39, 40, 49,
# 1, 8, 11, 18, 21, 28, 31, 38, 41, 48,
# 2, 7, 12, 17, 22, 27, 32, 37, 42, 47,
# 3, 6, 13, 16, 23, 26, 33, 36, 43, 46,
# 4, 5, 14, 15, 24, 25, 34, 35, 44, 45,

