from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import atexit
from led import Led

HOST = "0.0.0.0"
PORT = 9000

num_lights = 50
num_colors = 250
controller = Led(num_lights, num_colors)

class LEDServer(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself

		print(post_data)
		controller.decode(post_data)
		self._set_response()

def on_exit():
	server.server_close()
	print("Server stopped.")

if __name__ == "__main__":
	atexit.register(on_exit)

	controller.run()

	server = HTTPServer((HOST, PORT), LEDServer)
	print("Server started http://%s:%s" % (HOST, PORT))

	server.serve_forever()


	