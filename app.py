from flask import Flask , request
from flask_restful import Api
from flask_cors import CORS
from Controllers.StartUpClass import StartApp
from Controllers.NetworkClass import GetPicture
from Controllers.CameraController import CameraController
from flask_socketio import SocketIO, send
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")
api = Api(app)

api.add_resource(GetPicture, '/pic');
api.add_resource(StartApp, '/start');
api.add_resource(CameraController, '/camera');

@app.route('/msg')
def send_message():
    image = request.args.get('image')
    socketio.emit("message", image)
    return "I got you."

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

if __name__ == '__main__':
    app.run(debug=True)
