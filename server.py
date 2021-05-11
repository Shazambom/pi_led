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

num_lights = 50
num_colors = 250

#Uploader works great, only problem: we have no way of really making new frames... gotta brainstorm on an easy way to make new frames instead of just programming new ways.

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
		return make_tree(uploads_dir)

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
		for f in request.form:
			with open(os.path.join(uploads_dir, f), "rb") as frames:
				board.put(frames.read())
		return render_template('play.html', data=files)
	elif request.method == 'GET':
		return render_template('play.html', data=files)

@app.route('/rainbow', methods = ['GET'])
def rainbow():
	g = Generator(num_lights, num_colors)
	e = Encoder(num_lights, num_colors)
	rainbow = g.generate_rainbow_frames(250)
	frames = e.encode(rainbow)
	board.put(frames)
	return redirect(url_for('play'))

@app.route('/flow', methods = ['GET'])
def flow():
	g = Generator(num_lights, num_colors)
	e = Encoder(num_lights, num_colors)
	flow = g.generate_flow_frames(250)
	frames = e.encode(flow)
	board.put(frames)
	return redirect(url_for('play'))

@app.route('/dot', methods = ['GET'])
def dot():
	g = Generator(num_lights, num_colors)
	e = Encoder(num_lights, num_colors)
	dot = g.generate_dot_frames(250)
	frames = e.encode(dot)
	board.put(frames)
	return redirect(url_for('play'))

@app.route('/text', methods = ['GET', 'POST'])
def text():
	if request.method == 'POST':
		font = Font(5, int(num_lights / 5))
		e = Encoder(num_lights, num_colors)
		board.put(e.encode(font.text_to_frames(request.form['text'])))
	else:
		return render_template('text.html')




if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)