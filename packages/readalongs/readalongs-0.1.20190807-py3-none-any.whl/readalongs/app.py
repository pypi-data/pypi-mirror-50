''' ReadAlong Studio App '''

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "secret key"
# app.config['SESSION_PERMANENT'] = True
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# app.config['SESSION_FILE_THRESHOLD'] = 100

SOCKETIO = SocketIO(app)
import readalongs.views
