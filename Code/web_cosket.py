from flask import Flask, render_template
from flask_socketio import SocketIO,emit
from threading import Lock
import random
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

def background_thread():
    while True:
        socketio.sleep(5)
        t = random.randint(1, 100)
        socketio.emit('server_response',
                      {'data': t},namespace='/test_conn')


if __name__ == '__main__':
    socketio.run(app, debug=True,host='127.0.0.1',port=11000)
