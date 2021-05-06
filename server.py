from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
app = Flask(__name__, template_folder='./html')


uploads_dir = os.path.join('.', 'frames')
os.makedirs(uploads_dir, exist_ok=True)

#Uploader works great, only problem: we have no way of really making new frames... gotta brainstorm on an easy way to make new frames instead of just programming new ways.
#TODO integrate the LED player with this server: use the /play route that takes in a file name in a POST request. On the GET request of /play display all of the files that could be played as buttons that trigger the /play POST request.
#TODO add routes for generating rainbow, flow, and dot and storing them in the frames folder.
#TODO refactor rainbow, flow, and dot out of the encoder. Maybe have them inherit from the encoder? Not sure.



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






if __name__ == '__main__':
   app.run(debug = True)