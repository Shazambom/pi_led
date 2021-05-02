import board
import neopixel

num_lights = 50

pixels = neopixel.NeoPixel(board.D18, num_lights)

pixels[19] = (0, 255, 0)

pixels.fill((255, 0, 0))

pixels.fill((0,0,0))