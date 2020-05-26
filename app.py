from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from Controllers.StartUpClass import StartApp
from Controllers.NetworkClass import GetPicture
from Controllers.CameraController import CameraController
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

api.add_resource(GetPicture, '/pic');
api.add_resource(StartApp, '/start');
api.add_resource(CameraController, '/camera');


if __name__ == '__main__':
    app.run(debug=True)
