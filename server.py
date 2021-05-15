#!/usr/bin/python3
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
from generator import Generator
from encoder import Encoder
from led import Led
from font import Font
app = Flask(__name__, template_folder='./html')


uploads_dir = os.path.join('.', 'frames')
os.makedirs(uploads_dir, exist_ok=True)

num_lights = 100
num_colors = 250
screen_height = 5
DEFAULT_FPS = 60
DEFAULT_NUM_FRAMES = 250


board = Led(num_lights, num_colors)
board.run()

def make_tree(path):
    tree = dict(name=path, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree	

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_route():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(uploads_dir, secure_filename(f.filename)))
		return 'file uploaded successfully'
	elif request.method == 'GET':
		return render_template('upload.html')

def get_uploaded_files():
	children = make_tree(uploads_dir)["children"]
	files = []
	for child in children:
		files.append(child["name"].split('/')[-1])
	return files


@app.route('/play', methods = ['GET', 'POST'])
def play():
	files = get_uploaded_files()
	if request.method == 'POST':
		f = request.form["file"]
		fps = int(request.form["fps"])
		with open(os.path.join(uploads_dir, f), "rb") as frames:
			board.put(frames.read(), fps)
		return render_template('play.html', data=files)
	elif request.method == 'GET':
		if "func" in request.args:
			play_generated_frames(parse_args(request.args), request.args['func'])
		return render_template('play.html', data=files)

@app.route('/text', methods = ['GET', 'POST'])
def text():
	if request.method == 'POST':
		font = Font(screen_height, int(num_lights / screen_height))
		e = Encoder(num_lights, num_colors)
		board.put(e.encode(font.text_to_frames(request.form['text'])))
		return render_template('text.html')
	else:
		return render_template('text.html')

def play_generated_frames(args, func):
	g = Generator(num_lights, num_colors, screen_height)
	e = Encoder(num_lights, num_colors)

	frames = None
	if func == "rainbow":
		frames = g.generate_rainbow_frames(args['num_frames'])
	elif func == "flow":
		frames = g.generate_flow_frames(args['num_frames'])
	elif func == "dot":
		frames = g.generate_dot_frames(args['num_frames'])
	elif func == "radiate":
		frames = g.generate_radiate_frames(args['num_frames'])
	elif func == "cascade":
		frames = g.generate_cascade_frames()
	elif func == "snake":
		frames = g.generate_snake_frames()
	elif func == "game_of_life":
		frames = g.generate_game_of_life_frames(args['num_frames'])
	elif func == "wave":
		frames = g.generate_wave_frames(agrs['num_frames'])

	if frames is not None:
		board.put(e.encode(frames), args['fps'])

def parse_args(args):
	fps = DEFAULT_FPS
	num_frames = DEFAULT_NUM_FRAMES
	if 'fps' in args:
		try:
			fps = int(args['fps'])
		except ValueError:
			pass
	if 'num_frames' in args:
		try:
			num_frames = int(args['num_frames'])
		except ValueError:
			pass

	return {'fps': fps, 'num_frames': num_frames}


if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)