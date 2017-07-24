import os
from flask import Flask, request, redirect, url_for, flash

IMG_NAME = 'image.jpg'
OUT_FILE = './image.jpg'
ALLOWED_EXTENSIONS = set(['jpg'])




class Server:
    def __init__(self):
        app = Flask(__name__)
        app.config['onupload'] = self.handler
        @app.route('/upload', methods=['POST', 'GET'])
        def upload_file():
            if request.method == 'POST':
                # check if the post request has the file part
                if IMG_NAME not in request.files:
                    return redirect(request.url)
                file = request.files[IMG_NAME]
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    return redirect(request.url)

                file.save(OUT_FILE)
                app.config['onupload'](OUT_FILE)
                return 'ok'
            if request.method == 'GET':
                return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form method=post enctype=multipart/form-data>
                  <p><input type=file name=file>
                     <input type=submit value=Upload>
                </form>
                '''

        self.app = app

    def handler(self, fname):
        if not self.handlerfunc:
            print("Handlerfunc not defined")
        else:
            self.handlerfunc(fname)


    def run(self, host):
        self.app.run(host=host)


    def set_handlerfunc(self, f):
        self.handlerfunc = f



def hi_handler(fname):
    print("Upload complete", fname)

if __name__ == '__main__':
    srv = Server()
    srv.set_handlerfunc(hi_handler)
    srv.run('0.0.0.0')
