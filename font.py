import json
from PIL import Image, ImageDraw

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

#TODO: Still need to get the begining of the frames to start with off leds so the text scrolls past properly
	def TextToFrames(self, text):
		if not text.isalnum():
			return [[]]
		font_arr = []
		for char in text.upper():
			font_arr.append(self.font[char])
		num_frames = (self.font["width"] * len(text))
		frames = []

		slices = []
		num_slices = num_frames * self.width
		for i in range(num_slices):
			letter = int(i / self.font["width"])
			rem = i % self.font["width"]
			sl = []
			for i in range(self.font["height"]):
				for j in range(self.font["width"]):
					if rem == j:
						if letter < len(font_arr):
							sl.append(font_arr[letter][i][j])
						else:
							sl.append(0)
			slices.append(sl)

		for i in range(num_slices):
			frame = [off] * (self.height * self.width)
			for y in range(self.height):
				for x in range(self.width):
					if i + x < num_slices:
						sl = slices[i + x]
						loc = x*self.height + y
						if sl[y] == 1:
							frame[loc] = white
			frames.append(frame)
		return frames


font = Font(5, 50)
frames = font.TextToFrames('thequickfoxjumpedoverthelazydog1234567890')
images = []
for frame in frames:
	image = Image.new('RGB', (50, 5), off)
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			loc = i*5 + j
			image.putpixel((i, j), frame[loc])
	images.append(image)

images[0].save('font_experiment.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)





# 	<----------			<----------
# 0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
# 1, 6, 11, 16, 21, 26, 31, 36, 41, 46,
# 2, 7, 12, 17, 22, 27, 32, 37, 42, 47,
# 3, 8, 13, 18, 23, 28, 33, 38, 43, 48,
# 4, 9, 14, 19, 24, 29, 34, 39, 44, 49,