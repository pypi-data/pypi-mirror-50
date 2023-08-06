''' ReadAlong Studio web application views '''
import os
from pathlib import Path
from flask import abort, flash, redirect, request, render_template, url_for
from flask_socketio import emit
from werkzeug.utils import secure_filename

from readalongs.app import app, SOCKETIO
from readalongs.lang import get_langs

ALLOWED_TEXT = ['txt', 'xml', 'docx']
ALLOWED_AUDIO = ['wav', 'mp3']
ALLOWED_G2P = ['csv', 'xlsx']
ALLOWED_EXTENSIONS = set(ALLOWED_AUDIO + ALLOWED_G2P + ALLOWED_TEXT)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# TODO: This is currently just uploading everything to tmp...this is not good. more sophisticated option is needed!
app.config['UPLOAD_FOLDER'] = '/tmp/rastudio'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def uploaded_files():
    upload_dir = Path(app.config['UPLOAD_FOLDER'])
    audio = list(upload_dir.glob('*.wav')) + list(upload_dir.glob('*.mp3'))
    text = list(upload_dir.glob('*.txt')) + \
        list(upload_dir.glob('*.xml')) + list(upload_dir.glob('*.docx'))
    maps = list(upload_dir.glob('*.csv')) + list(upload_dir.glob('*.xlsx'))
    return {'audio': [{'path': str(x), 'fn': os.path.basename(str(x))} for x in audio],
            'text': [{'path': str(x), 'fn': os.path.basename(str(x))} for x in text],
            'maps': [{'path': str(x), 'fn': os.path.basename(str(x))} for x in maps]}


@app.route('/')
def home():
    ''' Home View - go to Step 1 '''
    return redirect(url_for('steps', step=1))


@SOCKETIO.on('remove event', namespace='/file')
def remove_f(message):
    path_to_remove = message['data']['path_to_remove']
    if os.path.exists(path_to_remove) and os.path.isfile(path_to_remove):
        os.remove(path_to_remove)
    emit('remove response', {'data': {'removed_file': os.path.basename(path_to_remove)}})

# @SOCKETIO.on('upload event' namespace='file')
# def upload_f(message):



@app.route('/remove', methods=['POST'])
def remove_file():
    if request.method == 'POST':
        path = request.data.decode('utf8').split('=')[1]
        os.remove(path)
    return redirect(url_for('steps', step=1))


@app.route('/step/<int:step>')
def steps(step):
    ''' Go through steps '''
    if step == 1:
        return render_template('upload.html', uploaded=uploaded_files(), maps=get_langs())
    elif step == 2:
        return render_template('preview.html')
    elif step == 3:
        return render_template('export.html')
    else:
        abort(404)


@app.route('/step/1', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'text' in request.files:
            # handle audio
            upfile = request.files['text']
        elif 'audio' in request.files:
            # handle audio
            upfile = request.files['audio']
        elif 'map' in request.files:
            # handle g2p
            upfile = request.files['map']
        else:
            flash('No file part')
            return redirect(request.url)
        filename = secure_filename(upfile.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        upfile.save(path)
        flash("File '%s' successfully uploaded" % filename)
        return redirect(request.url)

# with TemporaryDirectory() as tmpdir():

# fd, path = mkstemp()
#             try:
#                 document.save(path)
#                 return send_file(path,
#                                 as_attachment=True,
#                                 mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#                                 attachment_filename='conjugations.docx')
#             finally:
#                 os.remove(path)
