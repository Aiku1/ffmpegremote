#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
import ffmpeg
import subprocess

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'mov', 'avi'}

if not os.path.isdir('uploads/'):
    os.makedirs('uploads/')

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static", static_folder='/home/user/ffmpegremote/static')
app.secret_key="xeRkxtIsvphE4/s+"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["DEBUG"] = True

def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.after_request
def cleanup(response):
    shutil.rmtree('uploads/')
    os.makedirs('uploads/')
    return response

@app.route('/', methods=['GET'])
def display_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']

    if 'file' not in request.files or not file or file.filename == '' or not allowed_file(str(file.filename)):
        return redirect(request.url)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    file = file.filename
    outputfile = file[:file.find('.')] + "_out" + file[file.find('.'):]

    # if the requests comes from the GUI or has a fully qualified command, execute that
    if request.form['final_string']:
        ffmpegCommand = request.form['final_string']
        ffmpegProcess = subprocess.Popen(ffmpegCommand.split(), stdout=subprocess.PIPE)
        output, error = ffmpegProcess.communicate()
        
        if error:
            return redirect("")
    # if not, execute with single parameters
    else:
        filename = secure_filename(file.filename)
        bitrate = int(request.args.get("bitrate", 1))
        input_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        output_path = f"{app.config['UPLOAD_FOLDER']}/{outputfile}"
        (
            ffmpeg
            .input(input_path)
            .output(output_path, video_bitrate=str(bitrate)+'M')
            .overwrite_output()
            .run(quiet=True)
        )
       
    return send_from_directory('../' + app.config['UPLOAD_FOLDER'], outputfile, as_attachment=True)

app.run(host="0.0.0.0", port=80)
