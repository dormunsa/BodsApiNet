import jsonpickle
from Entity.Camera import Camera
from flask import request, Response, jsonify
from flask_restful import  Resource
from Logic.Camera import  *
import datetime


class CameraController(Resource):

    def post(self):

        data = request.json
        newCamera = Camera( 0 , data["LocationName"],(float)(data["Longitude"]),(float)(data["Latitude"]),data["IsWorking"],datetime.datetime.now())
        isSucceed = insertCameraLogic(newCamera)
        response = {'message': str(isSucceed)}
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    def get(self):
        cameraId = request.args.get('cameraId')
        cameraList = readCameraByIdLogic(cameraId)
        response_pickled = jsonpickle.encode(cameraList)
        return Response(response=response_pickled, status=200, mimetype="application/json")