import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'mov'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config["DEBUG"] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/render', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files or file.filename == '':
            flash('No file.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output = filename[:filename.rfind('.')+1] + 'out' + filename[filename.rfind('.'):]

            try:
                bitrate = requests.args.get('bitrate', '')
            except:
                try:
                    bitrate = requests.form['bitrate']
                except:
                    bitrate = 1

            bitrate = int(bitrate)

            subprocess.call('echo $(date) ffmpeg start; ffmpeg -y -hide_banner -loglevel panic -i {} -b {}M {}; echo $(date) ffmpeg end'.format(
                            app.config['UPLOAD_FOLDER'] + '/' + filename,
                            bitrate,
                            app.config['UPLOAD_FOLDER'] + '/' + output
                           ), shell=True)
            return send_from_directory(app.config['UPLOAD_FOLDER'], output, as_attachment=True)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file> <br>
      <input type=number placeholder=Bitrate (Mb/s) min=1 default=1 name=bitrate> <br>
      <input type=submit value=Upload>
    </form>
    '''

app.run(host="0.0.0.0", port=8081)
