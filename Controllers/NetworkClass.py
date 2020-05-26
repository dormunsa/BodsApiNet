import jsonpickle
from ThirdPartyServices.BODSAlerts import sendAlertToSlack
from NetworkConfiguration.Network import *
from flask import request , Response
from flask_restful import  Resource
from ThirdPartyServices.WeatherComponent import  *
from ThirdPartyServices.SMSAlert import  *
from ThirdPartyServices.Location import *
from Logic.Camera import *
from Logic.Detection import *
import boto3


#cahnge pic number for save detected images
def getPicIndex():
     global picIndex
     picIndex = picIndex + 1
     return picIndex



class GetPicture(Resource):

    def post(self):
        r = request
        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        # decode image
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))
        # Remove the bounding boxes with low confidence
        balloonDetected = postprocess(frame, outs)

        if(balloonDetected):
            index = getPicIndex()
            cv2.imwrite('./result/result_img' + str(index)+ '.jpg', frame.astype(np.uint8));
            #lat , lon = GettingLocation()
            cameraId = readCameraByLocation(32.098942,34.917123 )
            phone = readPhoneByCameraId(cameraId)
            hook = readHookByCameraId(cameraId)
            #sendAlertToSlack(hook)
            #sendSMSAlert(phone)
            weather = GetWeatherConditions(32.098942 , 34.917123)
            weatherId = BuildWeatherObjectAndPot(weather,32.098942 , 34.917123)
            InsertDetection(weatherId,cameraId,'https://detection-files-bods.s3.amazonaws.com/result_img' + str(index)+ '.jpg')
            # save frame in amazon
            s3 = boto3.client('s3')
            s3.upload_file('./result/result_img' + str(index)+ '.jpg', 'detection-files-bods', 'result_img' + str(index)+ '.jpg')

        # build a response dict to send back to client
        response = {'message': str(balloonDetected)}
        # encode response using jsonpickle
        response_pickled = jsonpickle.encode(response)

        return Response(response=response_pickled, status=200, mimetype="application/json")

    def get(self):
        return {"about" : "hello world"}