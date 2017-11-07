# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory
from werkzeug import secure_filename
from subprocess import call

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()+'/upload/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>Photo Upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
	    filename= 'in.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	    call(['./run_image_process.bash'], shell= True)
	    f= open('facedetect_result.txt')
	    lines= f.readlines()
	    f.close()
            file_url = url_for('uploaded_file', filename=filename)
            return html + '<br><img src=' + file_url + '>'+ '<div>'+ '{}'.format(lines)+'</div>'
    return html


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
