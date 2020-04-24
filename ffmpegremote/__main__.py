#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
import ffmpeg

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'mov'}

if not os.path.isdir('uploads/'):
    os.makedirs('uploads/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config["DEBUG"] = True

def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

@app.after_request
def cleanup(response):
    shutil.rmtree('uploads/')
    os.makedirs('uploads/')
    return response

@app.route('/render', methods=['GET'])
def display_form():
    return render_template('form.html')

@app.route('/render', methods=['POST'])
def upload_file():
    file = request.files['file']
    if 'file' not in request.files or file.filename == '':
        flash('No file.')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        output = filename[:filename.rfind('.')+1] + 'out' + filename[filename.rfind('.'):]
        bitrate = int(request.args.get("bitrate", 1))
        input_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        output_path = f"{app.config['UPLOAD_FOLDER']}/{output}"

        (
            ffmpeg
            .input(input_path)
            .output(output_path, video_bitrate=str(bitrate)+'M')
            .overwrite_output()
            .run(quiet=True)
        )

        return send_from_directory('../' + app.config['UPLOAD_FOLDER'], output, as_attachment=True)

app.run(host="0.0.0.0", port=8081)
