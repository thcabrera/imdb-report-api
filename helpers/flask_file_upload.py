from flask import request, abort
import os
import datetime
import time
import tempfile

def get_unix_timestamp():
    return time.mktime(datetime.datetime.now().timetuple())

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename, allowed_extensions):
    #if no extensions were specified, all extensions will be allowed
    if allowed_extensions == []:
        return True
    return '.' in filename and \
           get_extension(filename) in allowed_extensions

def get_file_from_request(app, allowed_extensions = []):
    # check if the post request has the file part
    if 'file' not in request.files:
        abort(400, 'No file part')
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        abort(400, 'No selected file')
    if file and allowed_file(file.filename, allowed_extensions):
        filename = str(get_unix_timestamp()) + '.' + get_extension(file.filename)
        # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filepath = os.path.join(tempfile.gettempdir(), filename)
        file.save(filepath)
        return filepath

